import socket
import threading

import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

from datetime import datetime
now = datetime.now()
time = now.strftime("%H:%M:%S")


HOST = '127.0.0.1'
PORT = 12000

class Client:

  def __init__(self, host, port):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.connect((host, port))

    msg = tkinter.Tk()
    msg.withdraw()

    self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent=msg)
    self.nickname = self.nickname.capitalize()

    self.gui_done = False
    self.running = True

    gui_thread = threading.Thread(target=self.gui_loop)
    recieve_thread = threading.Thread(target=self.receive)

    gui_thread.start()
    recieve_thread.start()

  def gui_loop(self):
    self.win = tkinter.Tk()
    self.win.configure(bg='lightgray')
    self.win.title(f"{self.nickname}'s chat room!")

    self.chat_label = tkinter.Label(self.win, text='Chat:', bg='lightgray')
    self.chat_label.config(font=('Arial', 12))
    self.chat_label.pack(padx=20, pady=5)

    self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
    self.text_area.pack(padx=20, pady=5)
    self.text_area.config(state='disabled')

    self.msg_label = tkinter.Label(self.win, text=f"Message from {self.nickname}", bg='lightgray')
    self.msg_label.config(font=('Arial', 12))
    self.msg_label.pack(padx=20, pady=5)

    self.input_area = tkinter.Text(self.win, height=3)
    self.input_area.pack(padx=20, pady=5)

    self.send_button = tkinter.Button(self.win, text='Send', command=self.write)
    self.send_button.config(font=('Arial', 12))
    self.send_button.pack(padx=20, pady=5)


    self.gui_done = True 

    self.win.protocol('WM_DELETE_WINDOW', self.stop)

    self.win.mainloop()


  def write(self):
    message = f"{self.nickname} at {time}: {self.input_area.get('1.0', 'end')}"
    self.client.send(message.encode('ascii'))
    self.input_area.delete('1.0', 'end')


  def stop(self):
    self.running = False
    self.win.destroy()
    self.client.close()
    exit(0)

  def receive(self):
    while self.running:
      try:
        message = self.client.recv(1024).decode('ascii')
        if message == 'Enter your Nickname:':
          self.client.send(self.nickname.encode('ascii'))
        else:
          if self.gui_done:
            self.text_area.config(state='normal')
            self.text_area.insert('end', message)
            self.text_area.yview('end')
            self.text_area.config(state='disabled')

      except ConnectionAbortedError:
        break
      except:
        print('Error occured')
        self.client.close()
        break



client = Client(HOST, PORT)

# recieve_thread = threading.Thread(target=recieve)
# recieve_thread.start()

# write_thread = threading.Thread(target=write)
# write_thread.start()
import socket
import threading

HOST = '127.0.0.1'
PORT = 12000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

server.listen()

clients = []
nicknames = []

def broadcast(message):
  for client in clients:
    client.send(message)

def handle(client):
  while True:
    try:
      message = client.recv(1024)
      broadcast(message)
    except:
      index = clients.index(client)
      clients.remove(client)
      client.close()
      nickname = nicknames[index]
      broadcast(f'{nickname} has left the room'.encode('ascii'))
      nicknames.remove(nickname)
      break

def recieve():
  while True:
    client, address = server.accept()

    client.send(f'Enter your Nickname:'.encode('ascii'))
    nickname = client.recv(1024).decode('ascii')

    clients.append(client)
    nicknames.append(nickname)

    print(f'Connected with {address}')
    broadcast(f'Connected with {nickname}\n'.encode('ascii'))
    client.send(f'Connected to the chat!!\n'.encode('ascii'))

    thread = threading.Thread(target=handle, args=(client,) )
    thread.start()


print('Server is listening')
recieve()
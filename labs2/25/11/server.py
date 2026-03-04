import socket

HOST = '127.0.0.1'
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(2)

client1, addr1 = server.accept()
client2, addr2 = server.accept()

while True:

    msg1 = client1.recv(1024).decode()
    if msg1.lower() == "exit":
        break
    print(f"Клієнт 1: {msg1}")
    client2.send(msg1.encode())

    msg2 = client2.recv(1024).decode()
    if msg2.lower() == "exit":
        break
    print(f"Клієнт 2: {msg2}")
    client1.send(msg2.encode())

server.close()

import socket

HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    msg = input("Ви: ")
    client.send(msg.encode())
    if msg.lower() == "exit":
        break

    reply = client.recv(1024).decode()
    print("Інший клієнт:", reply)

client.close()

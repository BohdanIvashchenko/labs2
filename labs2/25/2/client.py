import socket

HOST = '127.0.0.1'
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    expr = input("Введіть вираз (або exit): ")

    if expr.lower() == "exit":
        break

    client.sendall(expr.encode())
    data = client.recv(1024)

    print("Відповідь сервера:", data.decode())

client.close()
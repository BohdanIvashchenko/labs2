import socket
import re

HOST = '127.0.0.1'
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(2)

client, addr = server.accept()

allowed_pattern = re.compile(r'^[0-9+\-*/(). ]+$')

while True:
    data = client.recv(1024)
    if not data:
        break

    expression = data.decode().strip()

    if not allowed_pattern.fullmatch(expression):
        response = "Синтаксична помилка"
    else:
        try:
            result = eval(expression)
            response = str(result)
        except:
            response = "Синтаксична помилка"

    client.sendall(response.encode())

server.close()

import socket

HOST = '127.0.0.1'
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)
client, addr = server.accept()

while True:
    data = client.recv(1024)
    if not data:
        break

    expression = data.decode()

    try:
        result = eval(expression)
        response = f"{result}"
    except:
        response = "Синтаксична помилка"

    client.sendall(response.encode())

server.close()
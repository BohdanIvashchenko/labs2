import socket
import os

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5001

filepath = input("Введіть шлях до файлу: ")

client = socket.socket()
client.connect((SERVER_HOST, SERVER_PORT))

filename = os.path.basename(filepath)

# Відправляємо ім'я файлу
client.send(filename.encode())

# Невелика пауза щоб сервер встиг прийняти ім'я
import time
time.sleep(0.5)

# Відправляємо файл
with open(filepath, "rb") as f:
    while True:
        data = f.read(1024)
        if not data:
            break
        client.send(data)

print("Файл відправлено.")
client.close()
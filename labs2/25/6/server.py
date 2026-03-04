import socket
import os

HOST = '0.0.0.0'
PORT = 5001
SAVE_FOLDER = "uploads"

os.makedirs(SAVE_FOLDER, exist_ok=True)

server = socket.socket()
server.bind((HOST, PORT))
server.listen(1)

print("Сервер запущено. Очікування підключення...")

conn, addr = server.accept()
print("Підключено:", addr)

# Отримуємо ім'я файлу
filename = conn.recv(1024).decode()

# Отримуємо файл
with open(os.path.join(SAVE_FOLDER, filename), "wb") as f:
    while True:
        data = conn.recv(1024)
        if not data:
            break
        f.write(data)

print("Файл отримано.")
conn.close()
server.close()
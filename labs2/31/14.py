import os
import time
import random
import string
import shutil
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor

# Шляхи до каталогів
CATALOG1 = "Каталог1"
CATALOG2 = "Каталог2"
CATALOG3 = "Каталог3"

# Параметри
NUM_THREADS = 4  # кількість потоків для перевірки
CHECK_PATTERN = "шаблон"  # рядок для пошуку у файлах
FILE_GENERATION_INTERVAL = 2  # секунди між генераціями файлів
FILE_SIZE = 1024 * 1024  # розмір файлу ~1MB

# Створюємо каталоги, якщо їх нема
for directory in [CATALOG1, CATALOG2, CATALOG3]:
    os.makedirs(directory, exist_ok=True)


# --------------------------
# Підпроцес: генерує файли
# --------------------------
def generate_files():
    counter = 1
    while True:
        filename = f"file_{counter}.txt"
        filepath = os.path.join(CATALOG1, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            # Генеруємо великий текстовий файл
            text = ''.join(random.choices(string.ascii_letters + string.digits + " ", k=FILE_SIZE))
            # Додаємо випадково шаблон
            if random.random() < 0.5:
                text += f"\n{CHECK_PATTERN}\n"
            f.write(text)
        print(f"[Підпроцес] Створено файл: {filename}")
        counter += 1
        time.sleep(FILE_GENERATION_INTERVAL)


# --------------------------
# Функція для обробки файлу
# --------------------------
def process_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if CHECK_PATTERN in content:
            dest = CATALOG2
            print(f"[Потік] Файл {os.path.basename(file_path)} містить шаблон -> Каталог2")
        else:
            dest = CATALOG3
            print(f"[Потік] Файл {os.path.basename(file_path)} не містить шаблон -> Каталог3")
        shutil.move(file_path, os.path.join(dest, os.path.basename(file_path)))
    except Exception as e:
        print(f"[Помилка] Не вдалося обробити {file_path}: {e}")


# --------------------------
# Основний процес
# --------------------------
def main():
    # Запускаємо підпроцес
    generator_process = Process(target=generate_files)
    generator_process.start()

    # Множина для відстеження оброблених файлів
    processed_files = set()

    # Пул потоків
    with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
        while True:
            files = set(os.listdir(CATALOG1))
            new_files = files - processed_files
            if new_files:
                for file_name in new_files:
                    file_path = os.path.join(CATALOG1, file_name)
                    executor.submit(process_file, file_path)
                processed_files.update(new_files)
            time.sleep(1)  # невелика затримка, щоб не навантажувати CPU


if __name__ == "__main__":
    main()
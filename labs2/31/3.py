import threading
import time
import random
from collections import deque

queue = deque()
lock = threading.Lock()

t1 = 3
t2 = 4

def producer():
    i = 1
    while True:
        time.sleep(random.randint(1, t1))
        message = f"Message {i}"

        with lock:
            queue.append(message)
            print(f"Generated: {message}")

        i += 1


def consumer():
    while True:
        if queue:
            with lock:
                message = queue.popleft()

            print(f"Processing: {message}")
            time.sleep(random.randint(1, t2))
        else:
            time.sleep(0.5)


t_prod = threading.Thread(target=producer)
t_cons = threading.Thread(target=consumer)

t_prod.start()
t_cons.start()

t_prod.join()
t_cons.join()
import threading
import random
import time
from collections import deque

N = 10      # максимум кас
m = 3       # початкові касири
k = 15      # початкові покупці

t1 = 3      # інтервал приходу
t2 = 4      # час обслуговування
t3 = 10     # час до перерви
t4 = 5      # тривалість перерви

l_max = 8
threshold = 5

queues = [deque() for _ in range(N)]
locks = [threading.Lock() for _ in range(N)]

active = m
reserve = 0
max_queue = 0


def cashier(i):
    global max_queue

    while True:

        with locks[i]:
            if queues[i]:
                queues[i].popleft()
                service = random.randint(1, t2)
            else:
                service = None

        if service:
            time.sleep(service)
        else:
            time.sleep(0.5)

        with locks[i]:
            max_queue = max(max_queue, len(queues[i]))


def customers():
    global active, reserve

    while True:

        time.sleep(random.randint(1, t1))

        i = random.randint(0, active - 1)

        with locks[i]:
            queues[i].append(1)

            if len(queues[i]) > threshold and active < N:
                print("Відкрито резервну касу")

                threading.Thread(target=cashier, args=(active,), daemon=True).start()
                active += 1
                reserve += 1


def breaks():

    while True:

        time.sleep(random.randint(1, t3))

        i = random.randint(0, active - 1)
        print("Каса", i, "на перерві")

        time.sleep(random.randint(1, t4))


for i in range(k):
    queues[random.randint(0, m-1)].append(1)

for i in range(m):
    threading.Thread(target=cashier, args=(i,), daemon=True).start()

threading.Thread(target=customers, daemon=True).start()
threading.Thread(target=breaks, daemon=True).start()

time.sleep(60)

print("Максимальна довжина черги:", max_queue)
print("Резервних касирів використано:", reserve)
from collections import deque

class PriorityDeque:
    def __init__(self):
        self.queue = deque()

    def add_message(self, message, priority=False):
        if priority:
            self.queue.appendleft(message)
        else:
            self.queue.append(message)

    def get_message(self):
        if self.queue:
            return self.queue.popleft()
        return None

    def is_empty(self):
        return len(self.queue) == 0
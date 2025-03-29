from collections import deque

class Queue:
    env = {}

    def __init__(self):
        """Initialize an empty queue."""
        self.items = deque()

    def push(self, item):
        """Enqueue an item (add to the back of the queue)."""
        self.items.append(item)

    def pop(self):
        """Dequeue an item (remove from the front of the queue).
        Returns None if the queue is empty.
        """
        if self.items:
            return self.items.popleft()  # Remove from the front
        return None

    def index(self, index):
        """Return the item at the given index or None if out of range."""
        try:
            return self.items[index]
        except IndexError:
            return None

    def search(self, item):
        """Check if an item exists in the queue."""
        return item in self.items

    def size(self):
        """Return the number of items in the queue."""
        return len(self.items)
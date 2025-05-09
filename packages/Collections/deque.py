from collections import deque

class Deque:
    env = {}

    def __init__(self):
        """Initialize an empty deque."""
        self.items = deque()

    def pushFront(self, item):
        """Add an item to the front of the deque."""
        self.items.appendleft(item)

    def pushBack(self, item):
        """Add an item to the back of the deque."""
        self.items.append(item)

    def popFront(self):
        """Remove and return the front item of the deque. 
        Returns None if the deque is empty.
        """
        if self.items:
            return self.items.popleft()
        return None

    def popBack(self):
        """Remove and return the back item of the deque. 
        Returns None if the deque is empty.
        """
        if self.items:
            return self.items.pop()
        return None

    def index(self, index):
        """Return the item at the given index or None if out of range."""
        try:
            return self.items[index]
        except IndexError:
            return None

    def search(self, item):
        """Check if an item exists in the deque."""
        return item in self.items

    def size(self):
        """Return the number of items in the deque."""
        return len(self.items)
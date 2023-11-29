from collections import deque

class FixedSizeStack:
    def __init__(self, max_size):
        self.max_size = max_size
        self.container = deque(maxlen=max_size)

    def put(self, data):
        self.container.append(data)  # Append data to the right end of the deque

    def get(self):
        if not self.container:
            return None  # Return None if the container is empty
        return self.container[-1]  # Get the newest element from the right end of the deque

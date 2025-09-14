class queue():

    def __init__(self):
        self.queue = []
    def enqueue(self, item):
        self.queue.append(item)
    def isEmpty(self):
        return len(self.queue) == 0
    def dequeue(self):
        if self.isEmpty():
            print("Queue is empty")
        else:
            element = self.queue[0]
            self.queue = self.queue[1:]
            return element
from listQueue import ListQueue
import threading
import time

class Producer:
    def __init__(self, items, queue):
        self.__alive = True
        self.items = items
        self.pos = 0
        self.queue = queue

    def get_item(self):
        if self.pos < len(self.items):
            item = self.items[self.pos]
            self.pos += 1
            return item
        else:
            return None

    def run(self):
        while True:
            time.sleep(0.2)
            if self.__alive:
                item = self.get_item()
                if item:
                    self.queue.enqueue(item)
                    print("Arrived:", item.split()[1])
            else:
                break
        print("Producer is dying...")

    def finish(self):
        self.__alive = False

class Consumer:
    def __init__(self, queue):
        self.__alive = True
        self.queue = queue

    def run(self):
        while True:
            time.sleep(1)
            if self.__alive:
                if not self.queue.isEmpty():  
                    item = self.queue.dequeue()
                    print("Boarding:", item.split()[1])  
            else:
                break
        print("Consumer is dying...")

    def finish(self):
        self.__alive = False

def main():
    with open("customer.txt", "r") as file:
        customers = file.readlines()
    customers = [customer.strip() for customer in customers]

    queue = ListQueue()
    producer = Producer(customers, queue)
    consumer = Consumer(queue)

    producer_thread = threading.Thread(target=producer.run)
    consumer_thread = threading.Thread(target=consumer.run)

    producer_thread.start()
    consumer_thread.start()

    time.sleep(10) 
    producer.finish()
    consumer.finish()
    producer_thread.join()
    consumer_thread.join()

if __name__ == "__main__":
    main()

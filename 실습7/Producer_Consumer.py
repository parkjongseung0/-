from listQueue import ListQueue
import threading
import time

class Producer:
    def __init__(self,items):
        self.__alive=True
        self.items = items
        self.pos = 0
        self.worker = threading.Thread(target=self.run)

    def get_item(self):
        if self.pos < len(self.items):
            item = self.items[self.pos]
            self.pos +=1
            return item
        else:
            return None
        
    def run(self):
        while True:
            time.sleep(0.2)
            if self.__alive:
                item = self.get_item()
                print("Arrived:",item)
            else:
                break
        print("Producer is dying...")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()

class Consumer:
    def __init__(self):
        self.__alive = True
        self.worker = threading.Thread(target=self.run)

    def run(self):
        while True:
            time.sleep(1)
            if self.__alive:
                print("Boarding:")
            else:
                break
        print("Consumer is dying.")

    def start(self):
        self.worker.start()

    def finish(self):
        self.__alive = False
        self.worker.join()


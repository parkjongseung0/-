import threading
import time

class Passenger:
    def __init__(self, priority, name):
        self.priority = priority
        self.name = name

class PriorityQueues:
    def __init__(self, num_queues):
        self.queues = [[] for _ in range(num_queues)]

    def enqueue(self, passenger):
        self.queues[-passenger.priority].append(passenger)  # 등급이 높을수록 우선순위가 높음

    def dequeue(self):
        for queue in self.queues:
            if queue:
                return queue.pop(0)
        return None

class Producer:
    def __init__(self, passengers, queues):
        self.__alive = True
        self.passengers = passengers
        self.queues = queues

    def run(self):
        for passenger in self.passengers:
            time.sleep(0.2)
            if not self.__alive:
                break
            self.queues.enqueue(passenger)
            print("Arrived:", passenger.name)
            

    def finish(self):
        self.__alive = False

class Consumer:
    def __init__(self, queues):
        self.__alive = True
        self.queues = queues

    def run(self):
        while True:
            time.sleep(1)
            if not self.__alive:
                break
            passenger = self.queues.dequeue()
            if passenger:
                print("Boarding:", passenger.name)
            else:
                break
        print("Consumer is dying.")

    def finish(self):
        self.__alive = False

def main():
    with open("customer.txt", "r") as file:
        customers = file.readlines()
    customers = [customer.strip().split() for customer in customers]
    passengers = [Passenger(int(customer[0]), customer[1]) for customer in customers]

    queues = PriorityQueues(num_queues=6)  # 등급이 1부터 5까지이므로 6개의 큐를 사용

    producer = Producer(passengers, queues)
    consumer = Consumer(queues)

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

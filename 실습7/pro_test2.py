import threading
import time
import queue

class Producer:
    def __init__(self, items, q):
        self.__alive = True  # 생산자의 활성 상태를 나타내는 프라이빗 변수
        self.items = items  # 아이템 목록
        self.pos = 0  # 아이템 목록을 순회하기 위한 위치 인덱스
        self.queue = q  # 생산된 아이템을 저장할 큐

    def get_item(self):
        """아이템 목록에서 다음 아이템을 가져오는 메서드"""
        if self.pos < len(self.items):
            item = self.items[self.pos]
            self.pos += 1
            return item
        else:
            return None

    def run(self):
        """생산자의 실행 메서드"""
        while True:
            time.sleep(0.2)  # 잠시 대기
            if self.__alive:
                item = self.get_item()  # 다음 아이템 가져오기
                if item:
                    priority = self.determine_priority(item)  # 아이템의 우선순위 결정
                    self.queue.put((-priority, item))  # 아이템과 음수 우선순위를 큐에 넣어서 큰 숫자가 먼저 나오도록 함
                    print("Arrived:", item.split()[1])  # 도착한 고객 이름 출력
            else:
                break
        print("Producer is dying...")

    def finish(self):
        """생산자 종료 메서드"""
        self.__alive = False

    def determine_priority(self, item):
        """아이템의 우선순위를 결정하는 메서드"""
        customer_grade = int(item.split()[0])  # 등급을 정수로 변환
        return customer_grade

class Consumer:
    def __init__(self, q):
        self.__alive = True  # 소비자의 활성 상태를 나타내는 프라이빗 변수
        self.queue = q  # 생산자가 생성한 아이템을 소비할 큐

    def run(self):
        """소비자의 실행 메서드"""
        while True:
            time.sleep(1)  # 잠시 대기
            if self.__alive:
                if not self.queue.empty():
                    priority, item = self.queue.get()  # 우선순위와 아이템을 튜플로부터 가져오기
                    print("Boarding:", item.split()[1])  # 탑승한 고객 이름 출력
            else:
                break
        print("Consumer is dying.")

    def finish(self):
        """소비자 종료 메서드"""
        self.__alive = False

def main():
    with open("customer.txt", "r") as file:
        customers = file.readlines()  # 파일에서 고객 정보 읽어오기
    customers = [customer.strip() for customer in customers]  # 각 줄의 양쪽 공백 제거

    q = queue.PriorityQueue()  # 우선순위 큐 생성
    producer = Producer(customers, q)  # 생산자 인스턴스 생성
    consumer = Consumer(q)  # 소비자 인스턴스 생성

    producer_thread = threading.Thread(target=producer.run)  # 생산자 스레드 생성
    consumer_thread = threading.Thread(target=consumer.run)  # 소비자 스레드 생성

    producer_thread.start()  # 생산자 스레드 시작
    consumer_thread.start()  # 소비자 스레드 시작

    time.sleep(10)  # 메인 스레드는 여기서 잠시 대기
    producer.finish()  # 생산자 종료
    consumer.finish()  # 소비자 종료
    producer_thread.join()  # 생산자 스레드가 종료될 때까지 기다림
    consumer_thread.join()  # 소비자 스레드가 종료될 때까지 기다림

if __name__ == "__main__":
    main()

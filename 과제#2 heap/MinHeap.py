class MinHeap:
    def __init__(self, *args):
        # 초기화 시 리스트를 받아서 저장하거나 빈 리스트로 초기화
        self.heap = list(args[0]) if args else []

    def insert(self, lpn, priority):
        # 새로운 요소를 삽입하고 힙 속성을 유지하기 위해 percolateUp 호출
        self.heap.append([lpn, priority])
        self._percolate_up(len(self.heap) - 1)

    def _percolate_up(self, index: int):
        # 부모와 우선순위를 비교하여 힙 속성을 유지하는 재귀 함수
        parent = (index - 1) // 2
        if index > 0 and self.heap[index][1] < self.heap[parent][1]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._percolate_up(parent)

    def deleteMin(self):
        # 최소값 삭제 및 힙 속성 유지를 위해 percolateDown 호출
        if not self.isEmpty():
            min_val = self.heap[0]
            last_element = self.heap.pop()
            if not self.isEmpty():
                self.heap[0] = last_element
                self._percolate_down(0)
            return min_val
        else:
            return None

    def _percolate_down(self, index: int):
        # 자식과 우선순위를 비교하여 힙 속성을 유지하는 재귀 함수
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index
        if left < len(self.heap) and self.heap[left][1] < self.heap[smallest][1]:
            smallest = left
        if right < len(self.heap) and self.heap[right][1] < self.heap[smallest][1]:
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._percolate_down(smallest)

    def min(self):
        # 최소값 반환
        return self.heap[0] if self.heap else None

    def isEmpty(self) -> bool:
        # 힙이 비어 있는지 확인
        return not self.heap

    def clear(self):
        # 힙을 비움
        self.heap.clear()

    def size(self) -> int:
        # 힙의 크기 반환
        return len(self.heap)

    def heapPrint(self):
        # 힙 출력
        if self.is_empty():
            print("Heap is empty")
        else:
            height = (len(self.heap) - 1).bit_length()
            max_width = 2 ** height - 1
            index = 0
            for level in range(1, height + 1):
                width = 2 ** (level - 1)
                for _ in range(width):
                    if index < len(self.heap):
                        print(f"{self.heap[index]:^2}", end=" ")
                        index += 1
                print()

    def reorder(self, index):
        # 힙 속성을 다시 유지하기 위해 요소 재배열
        parent = (index - 1) // 2
        if index > 0 and self.heap[index][1] < self.heap[parent][1]:
            self._percolate_up(index)
        else:
            self._percolate_down(index)

    def update_frequency(self, lpn):
        # 주어진 lpn에 대한 우선순위를 업데이트하고 힙 속성을 유지하기 위해 재배열
        for index, item in enumerate(self.heap):
            if item[0] == lpn:
                item[1] += 1
                self.reorder(index)
                return True
        return False

    def count_access(self, lpn) -> int:
        # 주어진 lpn의 액세스 횟수 반환
        return sum(1 for item in self.heap if item[0] == lpn)

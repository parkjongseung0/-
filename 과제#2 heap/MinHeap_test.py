from MinHeap import MinHeap

minheap = MinHeap()

# 요소 삽입
minheap.insert('a', 10)
minheap.insert('b', 5)
minheap.insert('c', 8)
minheap.insert('d', 18)


print("최소값", minheap.min())  # 예상 출력: ('b', 5)
print("요소 삭제:", minheap.deleteMin())  # 예상 출력: ('b', 5)
print("삭제후 최소값 확인:", minheap.min())  # 예상 출력: ('c', 8)

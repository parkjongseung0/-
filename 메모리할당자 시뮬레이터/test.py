import time

class Node:
    def __init__(self, key, size):
        self.key = key
        self.size = size
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def insert(self, root, key, size):
        if not root:
            return Node(key, size)
        elif key < root.key:
            root.left = self.insert(root.left, key, size)
        else:
            root.right = self.insert(root.right, key, size)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def delete(self, root, key):
        if not root:
            return root
        elif key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.size = temp.size
            root.right = self.delete(root.right, temp.key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def get_min_value_node(self, root):
        if root is None or root.left is None:
            return root
        return self.get_min_value_node(root.left)

    def get_best_fit(self, root, size):
        if not root:
            return None
        if root.size == size:
            return root
        elif root.size > size:
            left = self.get_best_fit(root.left, size)
            return left if left else root
        else:
            return self.get_best_fit(root.right, size)

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

class Allocator:
    def __init__(self):
        self.chunk_size = 16 * 1024  # 16KB
        self.arena = []  # 실제 할당된 메모리 청크의 시작 주소를 저장하는 리스트
        self.used_chunks = {}  # {id: (start, size)}
        self.free_chunks = None  # AVLTree for free chunks
        self.total_allocated = 0  # total allocated memory size
        self.start_time = time.time()

    def print_stats(self):
            total_arena_size_MB = len(self.arena) * self.chunk_size / (1024 * 1024)
            used_memory_MB = self.total_allocated / 1024 / 1024  # MB
            utilization = used_memory_MB / total_arena_size_MB
            print(f"Arena: {total_arena_size_MB:.2f} MB")
            print(f"In-use: {used_memory_MB:.2f} MB")
            print(f"Utilization: {utilization:.2f}")
            print(self.total_allocated)


    def malloc(self, id, size):
        node = self._find_best_fit(size)
        
        if node:
            start = node.key
            self.free_chunks = AVLTree().delete(self.free_chunks, node.key)
            self.used_chunks[id] = (start, size)
            self.total_allocated += size
        else:
            # Check if the last allocated chunk has enough space for the new allocation
            if self.arena and (self.chunk_size - (self.total_allocated % self.chunk_size)) >= size:
                start = (len(self.arena) - 1) * self.chunk_size + (self.total_allocated % self.chunk_size)
                self.used_chunks[id] = (start, size)
                self.total_allocated += size
            else:
                # Add a new chunk only if necessary
                new_chunk_start = len(self.arena) * self.chunk_size
                self.arena.append([0] * self.chunk_size)
                self.used_chunks[id] = (new_chunk_start, size)
                self.total_allocated += size

    def free(self, id):
        if id in self.used_chunks:
            start, size = self.used_chunks.pop(id)
            self.total_allocated -= size
            self.free_chunks = self._insert_free_chunk(start, size)

    def _insert_free_chunk(self, start, size):
        return AVLTree().insert(self.free_chunks, start, size) if self.free_chunks else Node(start, size)

    def _find_best_fit(self, size):
        return AVLTree().get_best_fit(self.free_chunks, size) if self.free_chunks else None

if __name__ == "__main__":
    allocator = Allocator()
    start_time=time.time()
    # 테스트 케이스 추가
    test_requests = [
            ('a', 1, 1024),
            ('a', 2, 2048),
            ('a', 3, 3072),
            ('a', 4, 4096),
            ('f', 2),
            ('a', 5, 1536),
            ('f', 1),
            ('a', 6, 512),
            ('a', 7, 7168),
            ('f', 4),
            ('a', 8, 1024),
            ('a', 9, 4096),
            ('a', 10, 6144),
            ('a', 11, 2048),
            ('a', 12, 4096),
            ('a', 13, 2048),
            ('a', 14, 1024)
        ]

    for req in test_requests:
        if req[0] == 'a':
            allocator.malloc(req[1], req[2])
        elif req[0] == 'f':
            allocator.free(req[1])
        # print(req)
    allocator.print_stats()
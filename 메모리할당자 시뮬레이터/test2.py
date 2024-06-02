import time

class Node:
    def __init__(self, key, size, color='RED'):
        self.key = key
        self.size = size
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(0, 0, 'BLACK')
        self.root = self.TNULL

    def insert(self, key, size):
        node = Node(key, size)
        node.left = node.right = node.parent = self.TNULL
        node.color = 'RED'

        y = None
        x = self.root

        while x != self.TNULL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y
        if y is None:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        if node.parent is None:
            node.color = 'BLACK'
            return

        if node.parent.parent is None:
            return

        self.fix_insert(node)

    def delete(self, key):
        self.delete_node_helper(self.root, key)

    def fix_insert(self, k):
        while k.parent.color == 'RED':
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u.color == 'RED':
                    u.color = 'BLACK'
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right
                if u.color == 'RED':
                    u.color = 'BLACK'
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 'BLACK'
                    k.parent.parent.color = 'RED'
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 'BLACK'

    def delete_node_helper(self, node, key):
        z = self.TNULL
        while node != self.TNULL:
            if node.key == key:
                z = node
            if node.key <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.rb_transplant(z, z.right)
        elif z.right == self.TNULL:
            x = z.left
            self.rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 'BLACK':
            self.fix_delete(x)

    def fix_delete(self, x):
        while x != self.root and x.color == 'BLACK':
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 'RED':
                    s.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 'BLACK' and s.right.color == 'BLACK':
                    s.color = 'RED'
                    x = x.parent
                else:
                    if s.right.color == 'BLACK':
                        s.left.color = 'BLACK'
                        s.color = 'RED'
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 'BLACK'
                    s.right.color = 'BLACK'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 'RED':
                    s.color = 'BLACK'
                    x.parent.color = 'RED'
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == 'BLACK' and s.right.color == 'BLACK':
                    s.color = 'RED'
                    x = x.parent
                else:
                    if s.left.color == 'BLACK':
                        s.right.color = 'BLACK'
                        s.color = 'RED'
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 'BLACK'
                    s.left.color = 'BLACK'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'BLACK'

    def rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

class Allocator:
    def __init__(self):
        self.chunk_size = 16 * 1024  # Base chunk size
        self.arena = 0  # Total memory allocated as an integer
        self.used_chunks = {}  # Maps id to (start, size)
        self.free_chunks = RedBlackTree()  # Red-Black Tree for managing free space
        self.size_map = {}  # HashMap for quick access to size-based chunks
        self.total_allocated = 0  # Total allocated memory size
        self.start_time = time.time()

    def request_chunk_from_os(self, size):
        necessary_size = ((size + self.chunk_size - 1) // self.chunk_size) * self.chunk_size
        start = self.arena
        self.arena += necessary_size
        self.add_free_chunk(start, necessary_size)
        return start

    def add_free_chunk(self, start, size):
        if size not in self.size_map:
            self.size_map[size] = []
        self.size_map[size].append(start)
        self.free_chunks.insert(start, size)

    def remove_free_chunk(self, start, size):
        if size in self.size_map and start in self.size_map[size]:
            self.size_map[size].remove(start)
            if not self.size_map[size]:
                del self.size_map[size]
        self.free_chunks.delete(start)

    def malloc(self, id, size):
        if size > self.chunk_size:
            start = self.arena
            self.arena += size
            self.used_chunks[id] = (start, size)
            self.total_allocated += size
            return

        best_fit_size = next((s for s in sorted(self.size_map.keys()) if s >= size), None)
        if best_fit_size is None:
            self.request_chunk_from_os(size)
            best_fit_size = next((s for s in sorted(self.size_map.keys()) if s >= size), None)

        if best_fit_size is not None:
            start = self.size_map[best_fit_size].pop(0)
            if not self.size_map[best_fit_size]:
                del self.size_map[best_fit_size]
            remaining_size = best_fit_size - size
            self.remove_free_chunk(start, best_fit_size)
            if remaining_size > 0:
                self.add_free_chunk(start + size, remaining_size)
            self.used_chunks[id] = (start, size)
            self.total_allocated += size
        else:
            print("Memory allocation failed for id:", id, "with size:", size)

    def free(self, id):
        if id in self.used_chunks:
            start, size = self.used_chunks.pop(id)
            self.total_allocated -= size
            self.add_free_chunk(start, size)  # 병합 없이 자유 목록에 청크 추가


    def merge_free_chunks(self, start, size):
        merged_start, merged_size = start, size
        left_node = self.get_adjacent_left_free_chunk(start)
        right_node = self.get_adjacent_right_free_chunk(start + size)

        if left_node:
            merged_start = left_node.key
            merged_size += left_node.size
            self.remove_free_chunk(left_node.key, left_node.size)

        if right_node:
            merged_size += right_node.size
            self.remove_free_chunk(right_node.key, right_node.size)

        self.add_free_chunk(merged_start, merged_size)

    def compact_arena(self):
        largest_free = self.free_chunks.get_largest_free_chunk()
        if largest_free and largest_free.key + largest_free.size == self.arena:
            self.arena -= largest_free.size
            self.remove_free_chunk(largest_free.key, largest_free.size)

    def get_adjacent_left_free_chunk(self, start):
        current = self.free_chunks.root
        closest = None
        while current != self.free_chunks.TNULL:
            if current.key + current.size == start:
                closest = current
                break
            elif current.key + current.size < start:
                current = current.right
            else:
                current = current.left
        return closest

    def get_adjacent_right_free_chunk(self, end):
        current = self.free_chunks.root
        closest = None
        while current != self.free_chunks.TNULL:
            if current.key == end:
                closest = current
                break
            elif current.key < end:
                current = current.right
            else:
                current = current.left
        return closest

    def print_stats(self):
        total_arena = self.arena / 1024 / 1024  # MB
        in_use = self.total_allocated / 1024 / 1024  # MB
        utilization = in_use / total_arena if total_arena > 0 else 0
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        print(f"Execution Time: {elapsed_time:.2f} seconds")
        print(f"Arena: {total_arena:.2f} MB")
        print(f"In-use: {in_use:.2f} MB")
        print(f"Utilization: {utilization:.2f}")
        #print(self.used_chunks)

if __name__ == "__main__":
    allocator = Allocator()
    with open("C://Users//parkj//OneDrive//바탕 화면//숭실대//2-1//자료구조//jaryogujo//메모리할당자 시뮬레이터//input.txt", "r") as file:
        n = 0
        for line in file:
            req = line.split()
            if req[0] == 'a':
                allocator.malloc(int(req[1]), int(req[2]))
            elif req[0] == 'f':
                allocator.free(int(req[1]))

            # if n % 1000 == 0:
            #     print(n, "...")
            
            n += 1
    
    allocator.print_stats()

# Execution Time: 2.26 seconds
# Arena: 163.05 MB
# In-use: 162.19 MB
# Utilization: 0.99
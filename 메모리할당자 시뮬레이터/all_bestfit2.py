import time

CHUNK_SIZE = 16 * 1024  # 16KB

class BestFitAllocator:
    def __init__(self):
        self.free_list = []  # List of (start, size) tuples
        self.allocated = {}  # id -> (start, size)
        self.next_chunk_start = 0  # Next chunk starting address
        self.arena = set()  # Set of allocated chunk start addresses

    def allocate_chunk(self):
        # Allocate a new chunk from OS
        chunk_start = self.next_chunk_start
        self.free_list.append((chunk_start, CHUNK_SIZE))
        self.next_chunk_start += CHUNK_SIZE
        self.arena.add(chunk_start)

    def return_unused_chunks(self):
        # Identify and return unused chunks to OS
        used_chunks = set(start // CHUNK_SIZE * CHUNK_SIZE for start, size in self.allocated.values())
        unused_chunks = self.arena - used_chunks

        for chunk_start in unused_chunks:
            self.free_list = [(start, size) for start, size in self.free_list if start < chunk_start or start >= chunk_start + CHUNK_SIZE]
            self.arena.remove(chunk_start)

    def malloc(self, id, size):
        if id in self.allocated:
            raise ValueError(f"ID {id} already allocated")

        # Find the best fit block
        best_fit = None
        best_fit_index = -1
        for i, (start, free_size) in enumerate(self.free_list):
            if free_size >= size and (best_fit is None or free_size < best_fit):
                best_fit = free_size
                best_fit_index = i

        if best_fit is not None:
            start, free_size = self.free_list[best_fit_index]
            self.allocated[id] = (start, size)
            if free_size == size:
                del self.free_list[best_fit_index]
            else:
                self.free_list[best_fit_index] = (start + size, free_size - size)
            return

        # No suitable free block found, allocate a new chunk
        self.allocate_chunk()
        self.malloc(id, size)  # Retry allocation

    def free(self, id):
        if id not in self.allocated:
            raise ValueError(f"ID {id} not allocated")

        start, size = self.allocated.pop(id)
        self.free_list.append((start, size))
        self.free_list.sort()  # Keep the free list sorted by start address
        self.merge_free_blocks()
        self.return_unused_chunks()

    def merge_free_blocks(self):
        if not self.free_list:
            return
        merged_list = []
        prev_start, prev_size = self.free_list[0]

        for start, size in self.free_list[1:]:
            if prev_start + prev_size == start:
                prev_size += size
            else:
                merged_list.append((prev_start, prev_size))
                prev_start, prev_size = start, size
        merged_list.append((prev_start, prev_size))
        self.free_list = merged_list

    def print_stats(self, start_time):
        total_arena = len(self.arena) * CHUNK_SIZE / 1024 / 1024  # MB
        in_use = sum(size for _, size in self.allocated.values()) / 1024 / 1024  # MB
        utilization = in_use / total_arena if total_arena > 0 else 0
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Execution Time: {elapsed_time:.2f} seconds")
        print(f"Arena: {total_arena:.2f} MB")
        print(f"In-use: {in_use:.2f} MB")
        print(f"Utilization: {utilization:.4f}")

if __name__ == "__main__":
    allocator = BestFitAllocator()
    
    start_time = time.time()
    
    with open("C://Users//parkj//OneDrive//바탕 화면//숭실대//2-1//자료구조//jaryogujo//메모리할당자 시뮬레이터//input.txt", "r") as file:
        n = 0
        for line in file:
            req = line.split()
            if req[0] == 'a':
                try:
                    allocator.malloc(int(req[1]), int(req[2]))
                except MemoryError as e:
                    print(f"MemoryError: {e} for id={req[1]}, size={req[2]}")
            elif req[0] == 'f':
                try:
                    allocator.free(int(req[1]))
                except ValueError as e:
                    print(f"ValueError: {e} for id={req[1]}")

            if n % 1000 == 0:
                print(n, "...")
            
            n += 1
    
    allocator.print_stats(start_time)

# Execution Time: 195.85 seconds
# Arena: 163.02 MB
# In-use: 162.19 MB
# Utilization: 0.9949
#청크 os
class Allocator:
    def __init__(self):
        self.chunk_size = 16 * 1024  # 16KB
        self.arena = {}  # 메모리 풀(arena), {시작 주소: 크기}
        self.free_space = []  # 해제된 공간을 관리하는 리스트 [시작 주소, 크기]

    def print_stats(self):
        arena_size = sum(self.arena.values())
        free_size = sum(space[1] for space in self.free_space)
        used_size = arena_size - free_size
        print("Arena: {:.2f} MB".format(arena_size / (1024 * 1024)))
        print("In-use: {:.2f} MB".format(used_size / (1024 * 1024)))
        if arena_size > 0:
            utilization = used_size / arena_size
            print("Utilization: {:.2f}".format(utilization))
        else:
            print("Utilization: 0")

    def allocate_chunk(self):
        # OS로부터 chunk_size 만큼의 메모리를 할당받습니다.
        # 여기에서는 단순히 더미 값을 반환하도록 구현합니다.
        return self.chunk_size

    def malloc(self, id, size):
        # 요청한 메모리의 크기를 조정합니다. (chunk_size의 배수로)
        size = ((size - 1) // self.chunk_size + 1) * self.chunk_size

        # 메모리 풀에서 사용 가능한 공간을 찾습니다.
        allocated = False
        for i, (start, space_size) in enumerate(self.free_space):
            if space_size >= size:
                # 공간을 찾았을 경우, 할당하고 나머지 공간을 free space에 추가합니다.
                self.arena[start] = size
                if space_size > size:
                    self.free_space[i] = (start + size, space_size - size)
                else:
                    del self.free_space[i]
                allocated = True
                break

        # 사용 가능한 공간을 찾지 못했을 경우, OS에게 새로운 chunk를 할당받습니다.
        if not allocated:
            new_chunk_size = self.allocate_chunk()
            if new_chunk_size >= size:
                # 할당받은 chunk가 충분한 경우
                start = max(self.arena.keys()) + self.arena[max(self.arena.keys())]
                self.arena[start] = size
                if new_chunk_size > size:
                    self.free_space.append((start + size, new_chunk_size - size))
                allocated = True
            else:
                print("Error: Not enough memory available.")

    def free(self, id):
        if id in self.arena:
            size = self.arena.pop(id)
            self.free_space.append((id, size))


if __name__ == "__main__":
    allocator = Allocator()
    
    with open("./input.txt", "r") as file:
        n = 0
        for line in file:
            req = line.split()
            if req[0] == 'a':
                allocator.malloc(int(req[1]), int(req[2]))
            elif req[0] == 'f':
                allocator.free(int(req[1]))

            if n % 100 == 0:
                print(n, "...")
            
            n += 1
    
    allocator.print_stats()

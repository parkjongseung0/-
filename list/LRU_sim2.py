from circularLinkedList import CircularLinkedList

class CacheSimulator:
    def __init__(self, cache_slots):
        self.cache_slots = cache_slots
        self.cache = CircularLinkedList()
        self.cache_hit = 0
        self.tot_cnt = 1

    def do_sim(self, page):
        if self.cache.size() < self.cache_slots:
            if self.cache.index(page) != -2:
                self.cache_hit += 1
            else:
                self.cache.append(page)
        else:
            if self.cache.index(page) != -2:
                self.cache.remove(page)
                self.cache.append(page)
                self.cache_hit += 1
            else:
                self.cache.remove(self.cache.getNode(0).item)
                self.cache.append(page)
        self.tot_cnt += 1

    def print_stats(self):
        print("cache_slot = ", self.cache_slots, "cache_hit = ", self.cache_hit, "hit ratio = ", self.cache_hit / self.tot_cnt)


if __name__ == "__main__":
    data_file = open("./linkbench.trc")
    lines = data_file.readlines()
    for cache_slots in range(100, 1001, 100):
        cache_sim = CacheSimulator(cache_slots)
        for line in lines:
            page = line.split()[0]
            cache_sim.do_sim(page)

        cache_sim.print_stats()
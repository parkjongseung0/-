from MinHeap import MinHeap

def lfu_sim(cache_slots):
    cache_hit = 0
    tot_cnt = 0
    acc = {}
    heap = MinHeap()
    data_file = open("C:\\Users\\parkj\\OneDrive\\바탕 화면\\숭실대\\2-1\\자료구조\\jaryogujo\\과제#2 heap\\linkbench.trc")
  
    for line in data_file.readlines():
        lpn = line.split()[0]
        acc[lpn] = acc.get(lpn, 0) + 1

        if heap.count_access(lpn) != 0:
            cache_hit += 1
            heap.update_frequency(lpn)
        else:
            if heap.size() >= cache_slots:
                heap.deleteMin()
            heap.insert(lpn, acc[lpn])  
        tot_cnt += 1

    print("cache_slot =", cache_slots, "cache_hit =", cache_hit, "hit ratio =", cache_hit / tot_cnt)

if __name__ == "__main__":
    for cache_slots in range(100, 1000, 100):
        lfu_sim(cache_slots)

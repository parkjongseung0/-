#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    char *item;
    struct Node *next;
} Node;

typedef struct CircularLinkedList {
    Node *head;
    int size;
} CircularLinkedList;
//circular를 초기화 시키는 함수
CircularLinkedList *initializeList() {
    CircularLinkedList *list = (CircularLinkedList *)malloc(sizeof(CircularLinkedList));
    list->head = NULL;
    list->size = 0;
    return list;
}
// 리스트에 새로운 노드를 추가시킴
void append(CircularLinkedList *list, char *item) {
    Node *newNode = (Node *)malloc(sizeof(Node));
    newNode->item = strdup(item);
    newNode->next = NULL;

    if (list->head == NULL) {
        list->head = newNode;
        newNode->next = list->head;
    } else {
        Node *temp = list->head;
        while (temp->next != list->head)
            temp = temp->next;
        temp->next = newNode;
        newNode->next = list->head;
    }
    list->size++;
}
// 리스트에서 특정 항목을 제거시킴
void removeItem(CircularLinkedList *list, char *item) {
    if (list->head == NULL)
        return;

    Node *current = list->head;
    Node *prev = NULL;

    do {
        if (strcmp(current->item, item) == 0) {
            if (prev == NULL) { // head에 있는 항목을 삭제하는 경우
                Node *last = list->head;
                while (last->next != list->head)
                    last = last->next;
                if (list->size == 1) {
                    free(list->head);
                    list->head = NULL;
                } else {
                    last->next = current->next;
                    free(current->item);
                    free(current);
                    list->head = last->next;
                }
            } else { // head를 제외한(중간이나 끝)에 있는 항목을 삭제하는 경우
                prev->next = current->next;
                free(current->item);
                free(current);
            }
            list->size--;
            return;
        }
        prev = current;
        current = current->next;
    } while (current != list->head);
}
//리스트에서 특정 항목속에 있는 인덱스를 찾는 함수
int indexOf(CircularLinkedList *list, char *item) {
    if (list->head == NULL)
        return -2;

    Node *current = list->head;
    int index = 0;

    do {
        if (strcmp(current->item, item) == 0)
            return index;
        index++;
        current = current->next;
    } while (current != list->head);

    return -2;
}

int size(CircularLinkedList *list) {
    return list->size;
}
//리스트 삭제
void destroyList(CircularLinkedList *list) {
    Node *current = list->head;
    Node *temp = NULL;

    if (list->head != NULL) {
        do {
            temp = current->next;
            free(current->item);
            free(current);
            current = temp;
        } while (current != list->head);
    }

    free(list);
}

typedef struct CacheSimulator {
    CircularLinkedList *cache;
    int cache_slots;
    int cache_hit;
    int tot_cnt;
} CacheSimulator;
//CacheSimulator 를 초기화 시킴
CacheSimulator *initializeCacheSimulator(int cache_slots) {
    CacheSimulator *cacheSimulator = (CacheSimulator *)malloc(sizeof(CacheSimulator));
    cacheSimulator->cache = initializeList();
    cacheSimulator->cache_slots = cache_slots;
    cacheSimulator->cache_hit = 0;
    cacheSimulator->tot_cnt = 1;
    return cacheSimulator;
}
//CacheSimulator 수행함수
void doSim(CacheSimulator *cacheSimulator, char *page) {
    if (size(cacheSimulator->cache) < cacheSimulator->cache_slots) {
        if (indexOf(cacheSimulator->cache, page) != -2) {
            cacheSimulator->cache_hit++;
        } else {
            append(cacheSimulator->cache, page);
        }
    } else {
        if (indexOf(cacheSimulator->cache, page) != -2) {
            removeItem(cacheSimulator->cache, page);
            append(cacheSimulator->cache, page);
            cacheSimulator->cache_hit++;
        } else {
            removeItem(cacheSimulator->cache, cacheSimulator->cache->head->item);
            append(cacheSimulator->cache, page);
        }
    }
    cacheSimulator->tot_cnt++;
}
//최종적인 통계값을 출력하는 함수
void printStats(CacheSimulator *cacheSimulator) {
    printf("cache_slot = %d, cache_hit = %d, hit ratio = %f\n",
           cacheSimulator->cache_slots,
           cacheSimulator->cache_hit,
           (float)cacheSimulator->cache_hit / cacheSimulator->tot_cnt);
}

void destroyCacheSimulator(CacheSimulator *cacheSimulator) {
    destroyList(cacheSimulator->cache);
    free(cacheSimulator);
}
//메인 함수
int main() {
    FILE *data_file = fopen("./linkbench.trc", "r");
    if (data_file == NULL) {
        perror("Error opening file");
        return -1;
    }

    char line[256];
// 캐시 슬롯 수를 100부터 1000까지 100씩 증가하면서 테스트함
    for (int cache_slots = 100; cache_slots <= 1000; cache_slots += 100) {
        rewind(data_file); 
        CacheSimulator *cache_sim = initializeCacheSimulator(cache_slots);
        while (fgets(line, sizeof(line), data_file)) {
      
            line[strcspn(line, "\n")] = 0;
            char *page;
            char *token = strtok(line, " ");
            while (token != NULL) {
                page = strdup(token);
                doSim(cache_sim, page);
                free(page);
                token = strtok(NULL, " ");
            }
        }
        printStats(cache_sim);
        destroyCacheSimulator(cache_sim);
    }

    fclose(data_file);
    return 0;
}

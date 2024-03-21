#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Define Circular Linked List Node
typedef struct Node {
    char *item;
    struct Node *next;
} Node;

// Define Circular Linked List
typedef struct CircularLinkedList {
    Node *head;
    int size;
} CircularLinkedList;

// Initialize Circular Linked List
CircularLinkedList *initializeList() {
    CircularLinkedList *list = (CircularLinkedList *)malloc(sizeof(CircularLinkedList));
    list->head = NULL;
    list->size = 0;
    return list;
}

// Append to Circular Linked List
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

// Remove from Circular Linked List
void removeItem(CircularLinkedList *list, char *item) {
    if (list->head == NULL)
        return;

    Node *current = list->head;
    Node *prev = NULL;

    do {
        if (strcmp(current->item, item) == 0) {
            if (prev == NULL) { // item is in head
                Node *last = list->head;
                while (last->next != list->head)
                    last = last->next;
                if (list->size == 1) {
                    free(list->head);
                    list->head = NULL;
                } else {
                    last->next = current->next;
                    free(current);
                    list->head = last->next;
                }
            } else {
                prev->next = current->next;
                free(current);
            }
            list->size--;
            return;
        }
        prev = current;
        current = current->next;
    } while (current != list->head);
}

// Get index of item in Circular Linked List
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

// Get size of Circular Linked List
int size(CircularLinkedList *list) {
    return list->size;
}

// Destroy Circular Linked List
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

// Define Cache Simulator
typedef struct CacheSimulator {
    CircularLinkedList *cache;
    int cache_slots;
    int cache_hit;
    int tot_cnt;
} CacheSimulator;

// Initialize Cache Simulator
CacheSimulator *initializeCacheSimulator(int cache_slots) {
    CacheSimulator *cacheSimulator = (CacheSimulator *)malloc(sizeof(CacheSimulator));
    cacheSimulator->cache = initializeList();
    cacheSimulator->cache_slots = cache_slots;
    cacheSimulator->cache_hit = 0;
    cacheSimulator->tot_cnt = 1;
    return cacheSimulator;
}

// Perform simulation in Cache Simulator
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

// Print statistics of Cache Simulator
void printStats(CacheSimulator *cacheSimulator) {
    printf("cache_slot = %d, cache_hit = %d, hit ratio = %f\n",
           cacheSimulator->cache_slots,
           cacheSimulator->cache_hit,
           (float)cacheSimulator->cache_hit / cacheSimulator->tot_cnt);
}

// Destroy Cache Simulator
void destroyCacheSimulator(CacheSimulator *cacheSimulator) {
    destroyList(cacheSimulator->cache);
    free(cacheSimulator);
}

int main() {
    FILE *data_file = fopen("./linkbench.trc", "r");
    if (data_file == NULL) {
        perror("Error opening file");
        return -1;
    }

    char line[256];
    while (fgets(line, sizeof(line), data_file)) {
        // Remove trailing newline character
        line[strcspn(line, "\n")] = 0;

        // Cache slots loop
        for (int cache_slots = 100; cache_slots <= 1000; cache_slots += 100) {
            CacheSimulator *cache_sim = initializeCacheSimulator(cache_slots);
            char *page = strtok(line, " ");
            while (page != NULL) {
                doSim(cache_sim, page);
                page = strtok(NULL, " ");
            }
            printStats(cache_sim);
            destroyCacheSimulator(cache_sim);
        }
    }

    fclose(data_file);
    return 0;
}

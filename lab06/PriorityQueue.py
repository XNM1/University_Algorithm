class PriorityQueue:
    def __init__(self, min_ = False):
        self.__queue = {}
        self.__min = min_

    def push(self, item, priority):
        self.__queue[item] = priority

    def get(self):
        priorities = list(self.__queue.values())
        if self.__min:
            ip = min(priorities)
        else:
            ip = max(priorities)
        for key, value in self.__queue.items():
            if value == ip:
                del self.__queue[key]
                return key

    def len(self):
        return len(self.__queue)

    def __str__(self):
        return str(self.__queue)
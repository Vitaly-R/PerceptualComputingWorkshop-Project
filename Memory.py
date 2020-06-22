class Memory:
    def __init__(self, size=16):
        self.__mem = list()
        self.size = size

    def append(self, o):
        self.__mem.append(o)
        self.__mem = self.__mem[-8:]

    def __contains__(self, item):
        return item in self.__mem

    def __getitem__(self, index):
        return self.__mem[index]

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < self.size:
            result = self.__mem[self.index]
            self.index += 1
            return result
        raise StopIteration

    def __len__(self):
        return len(self.__mem)
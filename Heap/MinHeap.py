from sys import stdin

class MinBinHeap:
    def __init__(self):
        self._heap = []
        self.KeyIdxDict = {}  # словарь, хранящий номера ключей в куче, для доступа О(1)

    def __iadd__(self, other):
        self._heap.append(other)
        self.KeyIdxDict[other[0]] = len(self) - 1
        return self

    def __delitem__(self, idx):
        if idx == len(self) - 1:  # если удаляется последний элемент
            new = self._heap.pop()  # вытаскиваем эл-т с конца листа
            self.KeyIdxDict.pop(new[0])  # удаляем из словаря {key: idx}
            return
        new = self._heap.pop()  # вытаскиваем эл-т с конца листа
        elem = self._heap[idx]  # запоминаем [key, value] по удаляемому индексу в листе
        newidx = self.KeyIdxDict.pop(elem[0])  # удаляем из словаря {key: idx} и запоминаем idx
        self._heap[idx] = new  # изменяем элемент в листе по данному idx
        self.KeyIdxDict[new[0]] = newidx  # изменяем индекс для перенесенного ключа на newidx
        return

    def __setitem__(self, idx, value):
        self._heap[idx] = value  # value = [key, val]

    def __getitem__(self, idx):
        return self._heap[idx]

    def __len__(self):
        return len(self._heap)

    # runs in log(n) time
    def push_heap(self, key, value):
        if self.KeyIdxDict.get(key) != None:
            return False
        self += [key, value]
        self.siftup(len(self) - 1)
        return True

    def min_in_heap(self):
        if not len(self):
            return False
        K = self[0][0]
        I = 0
        V = self[0][1]
        return [K, I, V]

    def max_in_heap(self):
        if not len(self):
            return False
        K = max(self.KeyIdxDict)
        I = self.KeyIdxDict[K]
        V = self[I][1]
        return [K, I, V]

    def delete_in_heap(self, key):
        if self.KeyIdxDict.get(key) == None:
            return False
        if len(self):
            newval = self[len(self)-1]
            curval = self[self.KeyIdxDict[key]]
            del self[self.KeyIdxDict[key]]
        if len(self):
            if newval[0] < curval[0]:
                self.siftup(self.KeyIdxDict[newval[0]])
            elif newval[0] > curval[0]:
                self.siftdown(self.KeyIdxDict[newval[0]])
        return True

    def extract(self):
        if len(self):
            res = self[0]
            self.delete_in_heap(self[0][0])
            return [res[0], res[1]]
        else:
            return False

    def swap(self, i, j):
        self.KeyIdxDict[self[i][0]], self.KeyIdxDict[self[j][0]] = self.KeyIdxDict[self[j][0]], self.KeyIdxDict[self[i][0]]
        self[i], self[j] = self[j], self[i]

    def set_heap(self, key, value):
        if self.KeyIdxDict.get(key) == None:
            return False
        self[self.KeyIdxDict[key]] = [key, value]
        return True

    def search_in_heap(self, key):
        if self.KeyIdxDict.get(key) != None:
            return [self.KeyIdxDict[key], self[self.KeyIdxDict[key]][1]]
        else:
            return False
        return

    # runs in log(n) time
    def siftdown(self, node):
        child = 2 * node + 1
        # base case, stop recursing when we hit the end of the heap
        if child > len(self) - 1:
            return
        # check that second child exists; if so find max
        if (child + 1 <= len(self) - 1) and (self[child + 1][0] < self[child][0]):
            child += 1
        # preserves heap structure
        if self[node][0] > self[child][0]:
            self.swap(node, child)
            self.siftdown(child)
        else:
            return

    # runs in log(n) time
    def siftup(self, node):
        parent = (node - 1) >> 1
        if self[parent][0] > self[node][0]:
            self.swap(node, parent)
        # base case; we've reached the top of the heap
        if parent <= 0:
            return
        else:
            self.siftup(parent)

def print_heap(heap):
    if len(heap) == 0:
        print('_')
        return
    print('['+str(heap[0][0])+' '+heap[0][1]+']')
    step = 1
    idx = 1
    while idx < len(heap):
        out = ''
        for i in range(2**step):
            parent = (idx - 1) >> 1
            out += '[{} {} {}] '.format(heap[idx][0], heap[idx][1], heap[parent][0])
            idx += 1
            if i == 2**step-1:
                print(out[:-1])
            elif idx == len(heap):
                for k in range(2**step - (i+1)):
                    out += '_ '
                print(out[:-1])
                break
        step += 1
    return

def spacecount(string):
    count = 0
    for i in range(len(string)):
        if string[i] == ' ':
            count += 1
    return count

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

MinHeap = MinBinHeap()

s = stdin.readline()
while (s):
    command = s.split()
    if len(command) == 3 and command[0] == 'add' and isint(command[1]) and spacecount(s) == 2:
        ok = MinHeap.push_heap(int(command[1]), command[2])
        if not ok:
            print('error')
    elif len(command) == 3 and command[0] == 'set' and isint(command[1]) and spacecount(s) == 2:
        ok = MinHeap.set_heap(int(command[1]), command[2])
        if not ok:
            print('error')
    elif len(command) == 2 and command[0] == 'delete' and isint(command[1]) and spacecount(s) == 1:
        ok = MinHeap.delete_in_heap(int(command[1]))
        if not ok:
            print('error')
    elif len(command) == 2 and command[0] == 'search' and isint(command[1]) and spacecount(s) == 1:
        res = MinHeap.search_in_heap(int(command[1]))
        if not res:
            print('0')
        else:
            print('1 {} {}'.format(res[0], res[1]))
    elif len(command) == 1 and command[0] == 'extract' and spacecount(s) == 0:
        res = MinHeap.extract()
        if not res:
            print('error')
        else:
            print('{} {}'.format(res[0], res[1]))
    elif len(command) == 1 and command[0] == 'min' and spacecount(s) == 0:
        res = MinHeap.min_in_heap()
        if not res:
            print('error')
        else:
            print('{} {} {}'.format(res[0], res[1], res[2]))
    elif len(command) == 1 and command[0] == 'max' and spacecount(s) == 0:
        res = MinHeap.max_in_heap()
        if not res:
            print('error')
        else:
            print('{} {} {}'.format(res[0], res[1], res[2]))
    elif len(command) == 1 and command[0] == 'print' and spacecount(s) == 0:
        print_heap(MinHeap)
    elif len(command):
        print('error')
    s = stdin.readline()
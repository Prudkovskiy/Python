"""
задача о ранце методом динамического программирования
"""
from sys import stdin

class knapsack:
    def __init__(self, max_weight=0):
        self.W = max_weight
        self.weight = [0]
        self.price = [0]
        # массив со всеми предметами, которые в конечном итоге вошли в рюкзак
        self.ans = []
        """
        создаем матрицу, каждый элемент которой это max_price(i,w) - 
        максимальная цена при выборе из первых i предметов, при этом 
        суммарный вес рюкзака не превышает w <= W
        """
        self.max_price = []
        self.weight_gcd = 1 # НОД всех весов предметов для сокращения размера матрицы (масштабирование)
        # # заполняем нулями первую строчку (вместимости 0..W), когда ни один предмет в рюкзак не кладем
        # self.max_price.append([0 for i in range(self.W+1)])

    def __iadd__(self, other):
        self.weight.append(other[0])
        self.price.append(other[1])
        # self.max_price.append([0 for i in range(self.W+1)])
        return self

    def gcd(self, a, b):
        while b:
            a, b = b, a % b
        return abs(a)

    def find_gcd(self):
        if len(self.weight)-1 >= 2:
            # НОД от весов первого и второго эл-ов
            self.weight_gcd = self.gcd(self.weight[1], self.weight[2])
        else:
            return

        for i in range(2, len(self.weight)-1):
            self.weight_gcd = self.gcd(self.weight_gcd, self.weight[i])

    def dyn_knapsack(self):
        # создаем матрицу с учетом масштабирования и заполняем ее 0
        self.find_gcd()
        cols = self.W // self.weight_gcd + 1  # вместимость 0..W (div НОД)
        rows = len(self.weight)  # i первых предметов от 0 до k
        for j in range(rows):
            self.weight[j] = self.weight[j] // self.weight_gcd
            self.max_price.append([0 for i in range(cols)])

        for i in range(rows):
            for j in range(cols):
                # print(self.weight[i])
                if self.weight[i] <= j:
                    # print("вместился")
                    self.max_price[i][j] = max(self.max_price[i-1][j],
                                               self.max_price[i-1][j-self.weight[i]] + self.price[i])
                else:
                    # print("не вместился")
                    self.max_price[i][j] = self.max_price[i-1][j]
        # print(self.max_price)
        self.find_answer(rows - 1, cols - 1)
        # self.knapsack_price(self.ans)
        # print(list(reversed(self.ans)))
        return [self.max_price[rows-1][cols-1], self.knapsack_weight(self.ans), list(reversed(self.ans))]

    def knapsack_weight(self, subjects):
        weight = 0
        for sub in subjects:
            weight += self.weight[sub] * self.weight_gcd
        return weight


    def find_answer(self, k, w):
        if self.max_price[k][w] == 0:
            return
        if self.max_price[k][w] == self.max_price[k-1][w]:
            self.find_answer(k - 1, w)
        else:
            self.ans.append(k)
            self.find_answer(k - 1, w - self.weight[k])

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

s = stdin.readline()
pack = knapsack()
while(s):
    data = s.split()
    if len(data) == 1 and isint(data[0]):
        pack = knapsack(int(data[0]))

    elif len(data) == 2:

        pack += [int(data[0]), int(data[1])]

    s = stdin.readline()

pack_weight, pack_price, subjects = pack.dyn_knapsack()
fist_line = str(pack_price) + " " + str(pack_weight)
print(fist_line)
for i in subjects:
    print(i)
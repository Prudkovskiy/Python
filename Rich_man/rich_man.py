"""
задача о сумасшедшем богаче
жадные алгоритмы и двоичная система счисления
"""

class moneybags:
    def __init__(self, accumulation=0):
        self.Money = accumulation
        self.ans = []

    """
    выбираем оптимальный вариант
    где количество действий будет меньше
    в двоичной системе
    единица - 2 операции: вычесть 1, разделить на 2
    ноль - одну операцию: разделить на 2
    первую единицу мы отбрасываем и считаем ее как за 1 действие
    переводим число миллионов в двоичную систему
    """
    def choose_branch(self, money): # когда money - нечетное число
        option1 = bin(money + 1)[2:]
        option2 = bin(money - 1)[2:]
        num_of_steps1 = (option1.count("1") - 1) + len(option1)
        num_of_steps2 = (option2.count("1") - 1) + len(option2)

        if num_of_steps1 < num_of_steps2:
            self.ans.append("dec")
            return money + 1
        elif num_of_steps1 > num_of_steps2:
            self.ans.append("inc")
            return money - 1
        else:
            if len(option1) > len(option2):
                self.ans.append("dec")
                return money + 1
            elif len(option1) < len(option2):
                self.ans.append("inc")
                return money - 1
            else:
                num_of_units1 = 0
                for i in option1[::-1][3:]:
                    if i == "1":
                        num_of_units1 += 1
                if num_of_units1 <= 2:
                    self.ans.append("inc")
                    return money - 1
                else:
                    self.ans.append("dec")
                    return money + 1

    def accumulation(self):
        while self.Money > 1:
            if self.Money % 2 == 0:
                optimal = bin(self.Money)[2:]
                dbls = 0
                for i in optimal[::-1]:
                    if i == "0":
                        dbls += 1
                    else:
                        break
                self.Money = self.Money // 2**dbls
                for d in range(dbls):
                    self.ans.append("dbl")
            if self.Money == 1:
                break
            self.Money = self.choose_branch(self.Money)

        if self.Money != 0:
            self.ans.append("inc")
        self.ans = list(reversed(self.ans))
        return self.ans


rich_man = moneybags(int(input()))
result = rich_man.accumulation()
for i in result:
    print(i)
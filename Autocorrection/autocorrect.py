"""
distance of the Dahmerau-Levenshtein
"""
from sys import stdin

class autocorrect:
    def __init__(self):
        self.dictionary = {} # словарь корректных слов

    def distance(self, a, b):
        "Calculates the Levenshtein-damerau distance between a and b"
        cols, rows = len(a)+1, len(b)+1
        if cols > rows:
            # Make sure cols <= rows, to use O(cols) space for 3 arrays
            a, b = b, a
            cols, rows = rows, cols

        current_row = [i for i in range(cols)] # 0,1,..cols - distance
        pre_previous_row = []
        for i in range(1, rows):
            if i >= 2:
                pre_previous_row = previous_row
            previous_row, current_row = current_row, [i]+[0]*(cols-1)

            for j in range(1, cols):
                add = current_row[j-1]+1
                delete = previous_row[j]+1
                change = previous_row[j-1]
                transposition = max(add, change, delete)
                if a[j-1] != b[i-1]:
                    change = change + 1
                if (i >= 2) and a[j-2] == b[i-1] and a[j-1] == b[i-2]:
                    transposition = pre_previous_row[j-2] + 1
                current_row[j] = min(add, delete, change, transposition)

        return current_row[cols-1]

    def init_dict(self, new_word):
        self.dictionary[new_word.lower()] = None

    def find_similar(self, word):
        word = word.lower()
        if word in self.dictionary:
            return True
        return False

    def correction(self, word):
        word = word.lower()
        correct = []
        for key in self.dictionary:
            dist = self.distance(key, word)
            if dist <= 1:
                correct.append(key)
        correct.sort()
        return correct


Levenshtein = autocorrect()
s = stdin.readline()
dict_size = 0
while(s):
    command = s.split()
    if len(command) == 1:
        dict_size = int(command[0])
        break
    s = stdin.readline()

word = stdin.readline()
while(word):
    word = word.rstrip("\n")
    if len(word) >= 1 and dict_size:
        Levenshtein.init_dict(word)
        dict_size -= 1

    elif len(word) >= 1:
        if Levenshtein.find_similar(word):
            print(word + " - ok")
        else:
            correct = Levenshtein.correction(word)
            if not correct:
                print(word + " -?")
            else:
                res = ', '.join(correct)
                print("{} -> {}".format(word, res))

    word = stdin.readline()
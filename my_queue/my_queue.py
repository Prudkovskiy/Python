import sys
from sys import stdin

def spacecount(string):
    count = 0
    for i in range(len(string)):
        if string[i] == ' ':
            count += 1
    return count

s1 = sys.argv[1]
f_in = open(s1, 'r')
s1 = sys.argv[2]
f_out = open(s1, 'w')

s = f_in.readline()
while (s):
    command = s.split()
    if len(command) == 2 and command[0] == 'set_size' and command[1].isdigit() and spacecount(s) == 1:
        StackSize = int(command.pop())
        Stack = [''] * StackSize
        break
    elif len(command):
        f_out.write('error\n')
    s = f_in.readline()

s = f_in.readline()
count = 0
while (s):
    command = s.split()
    if len(command) == 1 and command[0] == 'print' and spacecount(s) == 0:
        if count > 0:
            s = ''
            for i in range(count):
                s += Stack[i]+' '
            f_out.write(s[:-1] + '\n')
        else:
            f_out.write('empty\n')
    elif len(command) == 1 and command[0] == 'pop' and spacecount(s) == 0:
        if count == 0:
            f_out.write('underflow\n')
        else:
            count -= 1
            f_out.write(Stack[0] + "\n")

            i = 0
            while i < count:
                Stack[i] = Stack[i + 1]
                i += 1
            Stack[i] = ''

    elif len(command) == 2 and command[0] == 'push' and spacecount(s) == 1:
        if count == StackSize:
            f_out.write('overflow\n')
        else:
            X = command.pop()
            count += 1
            Stack[count - 1] = X
    elif len(command):
        f_out.write('error\n')
    s = f_in.readline()
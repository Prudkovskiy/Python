from math import log
from sys import stdin
from sys import stdout

import my_queue


class TreeNode:
    def __init__(self, key, value, parent=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = parent

    def get_parent_key(self):
        return self.parent.key

    def get_right(self):
        return self.right

    def get_left(self):
        return self.left

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value


class SplayTree:
    def __init__(self):
        self.root = None
        self.count = 0

    def get_root(self):
        return self.root

    def get_count_of_nodes(self):
        return self.count

    def Splay(self, node):
        while node != self.root:
            if node.parent == self.root:
                self.Zig(node)
            else:
                if node.parent.right == node and node.parent.parent.right == node.parent:
                    self.ZigZig(node)
                elif node.parent.left == node and node.parent.parent.left == node.parent:
                    self.ZigZig(node)
                else:
                    self.ZigZag(node)

    def Zig(self, node):
        if node.parent.left == node:
            node.parent.left = node.right
            if node.right:
                node.right.parent = node.parent
            node.right = node.parent

        if node.parent.right == node:
            node.parent.right = node.left
            if node.left:
                node.left.parent = node.parent
            node.left = node.parent

        tmp = node.parent.parent
        if tmp and tmp.right == node.parent:
            tmp.right = node
        elif tmp and tmp.left == node.parent:
            tmp.left = node
        else:
            self.root = node
        node.parent.parent = node
        node.parent = tmp

    def ZigZig(self, node):
        self.Zig(node.parent)
        self.Zig(node)

    def ZigZag(self, node):
        self.Zig(node)
        self.Zig(node)

    def add_node(self, key, value):
        self.count += 1
        if not self.root:
            self.root = TreeNode(key, value)
            return True

        node = self.root
        while True:
            if key > node.get_key() and not node.right:
                node.right = TreeNode(key, value, node)
                self.Splay(node.right)
                break
            elif key < node.get_key() and not node.left:
                node.left = TreeNode(key, value, node)
                self.Splay(node.left)
                break
            elif key > node.get_key():
                node = node.right
            elif key < node.get_key():
                node = node.left
            else:
                self.count -= 1
                return False
        return True

    def set(self, key, value):
        node = self.root
        while True:
            if not node:
                return False
            if key > node.get_key():
                node = node.get_right()
            elif key < node.key:
                node = node.get_left()
            else:
                node.value = value
                self.Splay(node)
                return True

    def delete(self, key):
        node = self.root
        while True:
            if not node:
                return False
            if key > node.get_key():
                node = node.get_right()
            elif key < node.get_key():
                node = node.get_left()
            else:
                tree.Splay(node)
                break

        L_tree = node.left
        R_tree = node.right
        self.count -= 1
        if L_tree:
            L_tree.parent = None
        if R_tree:
            R_tree.parent = None

        # предполагается левосторонняя реализация
        if not L_tree:
            self.root = R_tree
        elif not R_tree:
            self.root = L_tree
        # предполагается левосторонняя реализация
        else:
            self.root = L_tree
            max_node = self.max()
            self.Splay(max_node)
            self.root.right = R_tree
            if R_tree:
                self.root.right.parent = self.root
        return True

    def find(self, key):
        node = self.root
        prev_node = node
        while True:
            if not node:
                self.Splay(prev_node)
                return None
            if key > node.get_key():
                prev_node = node
                node = node.get_right()
            elif key < node.key:
                prev_node = node
                node = node.get_left()
            else:
                self.Splay(node)
                return node

    def max(self):
        node = self.root
        prev_node = node
        while node:
            prev_node = node
            node = node.get_right()
        return prev_node

    def min(self):
        node = self.root
        prev_node = node
        while node:
            prev_node = node
            node = node.get_left()
        return prev_node

def breadth_first_search(tr):
    q = my_queue()
    n = tree.get_count_of_nodes()
    root = tree.get_root()
    if not root:  # если нам пришел словарь {None: count}
        stdout.write('_\n')  # значит дерево пустое
        return
    stdout.write('[' + str(root.get_key()) + ' ' + root.get_value() + ']\n')
    n -= 1
    if n == 0:
        return

    if not root.get_left():
        q.put({None: 1})
    else:
        q.put(root.get_left())
    if not root.get_right():
        q.put({None: 1})
    else:
        q.put(root.get_right())

    count = 1  # счетчик уровня, отслеживает что нижний слой закончился
    nones_counter = 0  # счетчик None'ов, отслеживает
    step = 1
    stop = False
    out = ''
    i = 0

    while True:
        node = q.get()
        if type(node) == dict:
            count += node[None]
            nones_counter = node[None]*2
            q.put({None: nones_counter})
        else:
            n -= 1
            count += 1
            if not node.get_left():
                q.put({None: 1})
            else:
                q.put(node.get_left())
            if not node.get_right():
                q.put({None: 1})
            else:
                q.put(node.get_right())

        r = log(count + 1) / log(2)
        if n == 0 and r == int(r):
            stop = True

        if type(node) == dict:
            for k in range(node[None]):
                out += '_ '
                i += 1
        else:
            parent_key = node.get_parent_key()
            out += '[{} {} {}] '.format(node.get_key(), node.get_value(), parent_key)
            i += 1

        if i == 2 ** step:
            stdout.write(out[:-1] + '\n')
            out = ''
            i = 0
            step += 1

        if stop:
            break

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

tree = SplayTree()
s = stdin.readline()

while(s):
    command = s.split()
    if len(command) == 3 and command[0] == 'add' and isint(command[1]) and spacecount(s) == 2:
        ok = tree.add_node(int(command[1]), command[2])
        if not ok:
            print('error')

    elif len(command) == 3 and command[0] == 'set' and isint(command[1]) and spacecount(s) == 2:
        ok = tree.set(int(command[1]), command[2])
        if not ok:
            print('error')

    elif len(command) == 2 and command[0] == 'delete' and isint(command[1]) and spacecount(s) == 1:
        ok = tree.delete(int(command[1]))
        if not ok:
            print('error')

    elif len(command) == 2 and command[0] == 'search' and isint(command[1]) and spacecount(s) == 1:
        node = tree.find(int(command[1]))
        if not node:
            print('0')
        else:
            print("1 {}".format(node.get_value()))

    elif len(command) == 1 and command[0] == 'min' and spacecount(s) == 0:
        min_node = tree.min()
        if not min_node:
            print('error')
        else:
            print("{} {}".format(min_node.get_key(), min_node.get_value()))

    elif len(command) == 1 and command[0] == 'max' and spacecount(s) == 0:
        max_node = tree.max()
        if not max_node:
            print('error')
        else:
            print("{} {}".format(max_node.get_key(), max_node.get_value()))

    elif len(command) == 1 and command[0] == 'print' and spacecount(s) == 0:
        # nodes = breadth_first_search(tree)
        # print_tree(nodes)
        breadth_first_search(tree)

    elif len(command):
        print('error')

    s = stdin.readline()
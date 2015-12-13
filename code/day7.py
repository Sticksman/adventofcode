import bitstring
from functools import partial
import json


def preprocess(fn, *args):
    def new_fn(*args):
        self = args[0]
        args = args[1:]
        new_args = []
        for arg in args:
            if isinstance(arg, str):
                arg = self.symbols.get(arg)
                if arg is None:
                    raise ValueError("Not yet initialized")

            arg = bitstring.Bits(uint=arg, length=16)
            new_args.append(arg)
        return fn(self, *new_args)

    return new_fn

class Circuit(object):
    operations = [
        'and',
        'or',
        'lshift',
        'rshift',
        'not',
        'assign'
    ]

    @classmethod
    def parse_line(cls, line):
        line = line.lower()
        line = line.replace('->', 'assign')
        symbol_list = line.split(' ')

        p_tree = ParseTree()
        for symbol in symbol_list:
            node = ParseTreeNode(node_name=symbol)
            if symbol in cls.operations:
                node.left = p_tree.head
                p_tree.head = node
            else:
                if p_tree.head:
                    if not p_tree.head.left:
                        p_tree.head.left = node
                    else:
                        p_tree.head.right = node
                else:
                    p_tree.head = node

        return p_tree

    def __init__(self, circuit_file=None):
        self.symbols = {}
        self.trees = []
        self.circuit_file = circuit_file
        if self.circuit_file:
            self.parse_circuit_file(circuit_file)

    def parse_circuit_file(self, file_name):
        with open(file_name, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                p_tree = self.parse_line(line)
                self.trees.append(p_tree)

    def execute_tree(self, node):
        if node and node.node_name in self.operations:
            fn = '%s_fn' % node.node_name
            args = [self.execute_tree(node.left), self.execute_tree(node.right)]
            args = [arg for arg in args if arg is not None]
            return partial(getattr(self, fn), *args)
        elif node:
            return node.node_name
        else:
            return

    def execute_circuit(self, symbol=None):
        while bool(self.trees) or self.symbols.get(symbol):
            indexes = []
            for i, t in enumerate(self.trees):
                try:
                    fn = self.execute_tree(t.head)
                    fn()
                    indexes.append(i)
                except ValueError:
                    continue

            self.prune_trees(indexes)
            print self.trees

    def prune_trees(self, indexes):
        if indexes:
            print 'pruning'
        indexes.reverse()
        for i in indexes:
            self.trees.pop(i)

    @preprocess
    def and_fn(self, x, y):
        return (x & y).uint

    @preprocess
    def or_fn(self, x, y):
        return (x | y).uint

    @preprocess
    def lshift_fn(self, x, bit_count):
        return (x << bit_count.uint).uint

    @preprocess
    def rshift_fn(self, x, bit_count):
        return (x >> bit_count.uint).uint

    @preprocess
    def not_fn(self, x):
        return (~x).uint

    def assign_fn(self, value, symbol):
        if callable(value):
            value = value()
            print value
        elif isinstance(value, str):
            value = self.symbols.get(value)
            if not value:
                raise ValueError('Not yet assigned')

        self.symbols[symbol] = value


class ParseTree(object):
    def __init__(self, head=None):
        self.head = head

    def __repr__(self):
        return repr(self.head)


class ParseTreeNode(object):
    def __init__(self, node_name, left_node=None, right_node=None):
        self.node_name = node_name
        self.left = left_node
        self.right = right_node
        self.visited = False

    @property
    def node_name(self):
        return getattr(self, '_node_name', None)

    @node_name.setter
    def node_name(self, val):
        try:
            self._node_name = int(val)
        except ValueError:
            self._node_name = val

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(dict(
            node_name=self.node_name,
            left=self.left,
            right=self.right
        ))


if __name__ == '__main__':
    c = Circuit('adventofcode/inputs/day7')
    c.execute_circuit()
    # print c.symbols['a']

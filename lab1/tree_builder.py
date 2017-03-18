__author__ = 'alex'


class NodeType:
    Empty = 0
    Symbol = 1
    Cat = 2
    Star = 3
    Or = 4


class Node:
    def __init__(self):
        self.string = ""
        self.node_type = None

        self.left = None
        self.right = None
        self.parent = None

        self.pos = None
        self.nullable = None
        self.firstpos = []
        self.lastpos = []
        self.followpos = []

    def mark_positions(self, i):
        if self.string not in "*|.":
            self.pos = i+1
            return self.pos
        else:
            left_pos = self.left.mark_positions(i)
            if self.string == "*":
                result = left_pos
            else:
                result = self.right.mark_positions(left_pos)
            return result

    def calculate_nullable(self):
        if self.pos is not None:
            self.nullable = False
        elif self.node_type == NodeType.Star:
            self.nullable = True
            self.left.calculate_nullable()
        else:
            self.left.calculate_nullable()
            self.right.calculate_nullable()
            if self.node_type == NodeType.Or:
                self.nullable = self.left.nullable or self.right.nullable
            elif self.node_type == NodeType.Cat:
                self.nullable = self.left.nullable and self.right.nullable
            else:
                assert False, "Smth went wrong..."

    def calculate_firstpos(self):
        pass

    def calculate_followpos(self):
        pass

    def calculate_functions(self):
        self.mark_positions(0)
        self.calculate_nullable()
        self.calculate_firstpos()
        self.calculate_followpos()


def token_in_brackets(regexp, i):
    brackets_counter = 1
    j = i
    while brackets_counter != 0 and j < len(regexp):
        j += 1
        ch = regexp[j]
        if ch == "(":
            brackets_counter += 1
        elif ch == ")":
            brackets_counter -= 1

    assert j != len(regexp), "Incorrect brackets in regexp"
    return regexp[i+1:j], j


# inserts "." as cat operation when needed
def tokenize(regexp):
    tokens = []
    i = 0
    is_multiplier = False
    while i < len(regexp):
        ch = regexp[i]
        if ch == "(":
            token, i = token_in_brackets(regexp, i)
            if is_multiplier:
                tokens.append(".")
            tokens.append(token)
        else:
            if ch in "*|":
                tokens.append(ch)
            else:
                if is_multiplier:
                    tokens.append(".")
                tokens.append(ch)

        is_multiplier = ch != "|"
        i += 1

    return tokens


def build_tree(regexp):
    root = None
    left_set = False
    for token in tokenize(regexp):
        if len(token) > 1:  # expression in brackets
            node = build_tree(token)
        else:
            node = Node()
            node.string = token
            if token == "*":
                node.node_type = NodeType.Star
            elif token == "|":
                node.node_type = NodeType.Or
            elif token == ".":
                node.node_type = NodeType.Cat
            else:
                node.node_type = NodeType.Symbol

        if root is None:
            root = node
        elif left_set:
            root.right = node
            left_set = False
        else:
            assert node.string in "*|.", "Smth gets wrong"

            node.left = root
            if not node.node_type == NodeType.Star:
                left_set = True
            root = node

    return root


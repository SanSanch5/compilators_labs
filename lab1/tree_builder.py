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

    def calculate_functions(self):
        pass


def token_in_brackets(regexp, i):
    brackets_counter = 1
    token = ""
    j = i
    while not brackets_counter == 0 or j < len(regexp):
        j += 1
        ch = regexp(j)
        if ch == "(":
            brackets_counter += 1
            token += ch
        elif ch == ")":
            brackets_counter -= 1
            if not brackets_counter == 0:
                token += ch

    return token, j


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

        is_multiplier = True
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
            else:
                node.node_type = NodeType.Symbol

        if root is None:
            root = node
        elif left_set:
            root.right = node
            left_set = False
        else:
            assert node.string in "*|", "Smth gets wrong"

            node.left = root
            if not node.node_type == NodeType.Star:
                left_set = True
            root = node

    return root


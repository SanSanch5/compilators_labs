__author__ = 'alex'


class NodeType:
    Empty = 0
    Symbol = 1
    Cat = 2
    Star = 3
    Or = 4


PosToSymbolMap = dict()
FollowposMap = dict()


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

    def mark_positions(self, i):
        if self.string not in "*|.":
            self.pos = i+1
            PosToSymbolMap[self.pos] = self.string
            return self.pos
        else:
            left_pos = self.left.mark_positions(i)
            if self.string == "*":
                result = left_pos
            else:
                result = self.right.mark_positions(left_pos)
            return result

    def calculate_nullable_firstpos_and_lastpos(self):
        if self.pos is not None:
            self.nullable = False
            self.firstpos.append(self.pos)
            self.lastpos.append(self.pos)
        elif self.node_type == NodeType.Star:
            self.nullable = True
            self.left.calculate_nullable_firstpos_and_lastpos()
            self.firstpos = self.left.firstpos
            self.lastpos = self.left.lastpos
        else:
            self.left.calculate_nullable_firstpos_and_lastpos()
            self.right.calculate_nullable_firstpos_and_lastpos()
            self.firstpos.extend(self.left.firstpos)
            self.lastpos.extend(self.right.lastpos)
            if self.node_type == NodeType.Or:
                self.nullable = self.left.nullable or self.right.nullable
                self.firstpos.extend(self.right.firstpos)
                self.lastpos.extend(self.left.lastpos)
            elif self.node_type == NodeType.Cat:
                self.nullable = self.left.nullable and self.right.nullable
                if self.left.nullable:
                    self.firstpos.extend(self.right.firstpos)
                if self.right.nullable:
                    self.lastpos.extend(self.left.lastpos)
            else:
                assert False, "Smth went wrong..."

    def followpos(self, i):
        result = []
        if self.node_type == NodeType.Cat and i in self.left.lastpos:
            result = self.right.firstpos
        elif self.node_type == NodeType.Star and i in self.lastpos:
            result = self.left.firstpos

        if self.left is not None:
            result.extend(self.left.followpos(i))
        if self.right is not None:
            result.extend(self.right.followpos(i))

        return set(result)

    def calculate_functions(self):
        self.mark_positions(0)
        self.calculate_nullable_firstpos_and_lastpos()
        for key in PosToSymbolMap.keys():
            FollowposMap[key] = self.followpos(key)


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


# не учитывается приоритет операций, только скобки
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


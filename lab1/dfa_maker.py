__author__ = 'alex'

from tree_builder import build_tree


def make_dfa(regexp):
    expanded_regexp = regexp + "#"
    root = build_tree(expanded_regexp)
    root.calculate_functions()

    print(root.followpos(1))
    print(root.followpos(2))
    print(root.followpos(3))
    print(root.followpos(4))
    print(root.followpos(5))
    print(root.followpos(6))
    pass


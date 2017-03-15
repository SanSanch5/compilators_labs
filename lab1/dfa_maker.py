__author__ = 'alex'

from tree_builder import build_tree


def make_dfa(regexp):
    expanded_regexp = regexp + "#"
    root = build_tree(expanded_regexp)
    root.calculate_functions()
    pass


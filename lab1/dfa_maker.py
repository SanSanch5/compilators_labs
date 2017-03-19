__author__ = 'alex'

from tree_builder import build_tree, PosToSymbolMap, FollowposMap


def make_dfa(regexp):
    expanded_regexp = regexp + "#"
    root = build_tree(expanded_regexp)
    root.calculate_functions()

    print(PosToSymbolMap)
    print(FollowposMap)


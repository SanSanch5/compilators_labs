__author__ = 'alex'

from tree_builder import build_tree, PosToSymbolMap, FollowposMap


def make_dfa(regexp):
    assert "#" not in regexp, "Illegal symbol in regexp"

    expanded_regexp = regexp + "#"
    root = build_tree(expanded_regexp)
    root.calculate_functions()

    print(PosToSymbolMap)
    print(FollowposMap)

    alphabet = set(PosToSymbolMap.values()) - set("#")
    start = frozenset(root.firstpos)
    Dstates = dict()
    Dtran = dict()  # transformation table
    Dstates[start] = False
    while False in Dstates.values():
        # get unmarked state
        T = list(Dstates.keys())[list(Dstates.values()).index(False)]
        Dstates[T] = True
        for a in alphabet:
            U = set()
            for pos in [p for p in T if PosToSymbolMap[p] == a]:
                U = U.union(FollowposMap[pos])
            if bool(U) and frozenset(U) not in Dstates:
                Dstates[frozenset(U)] = False
            if T not in Dtran:
                Dtran[T] = dict()
            Dtran[T][a] = U

    states = list(Dstates.keys())
    pos_of_last_symbol = list(PosToSymbolMap.keys())[list(PosToSymbolMap.values()).index("#")]
    finite_states = [state for state in states if pos_of_last_symbol in state]

    return alphabet, start, states, Dtran, finite_states

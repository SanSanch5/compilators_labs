__author__ = 'alex'

from tree_builder import build_tree, PosToSymbolMap, FollowposMap


class DFA:
    def __init__(self):
        self.alphabet = None
        self.start_state = None
        self.states = None
        self.transformation_table = None
        self.finite_states = None
        self.minimized_states = None

    # напрямую из регулярки, без НКА
    def make(self, regexp):
        assert "#" not in regexp, "Illegal symbol in regexp"

        expanded_regexp = regexp + "#"
        root = build_tree(expanded_regexp)
        root.calculate_functions()

        self.alphabet = set(PosToSymbolMap.values()) - set("#")
        self.start_state = frozenset(root.firstpos)
        Dstates = dict()
        Dtran = dict()  # transformation table
        Dstates[self.start_state] = False
        while False in Dstates.values():
            # get unmarked state
            T = list(Dstates.keys())[list(Dstates.values()).index(False)]
            Dstates[T] = True
            for a in self.alphabet:
                U = set()
                for pos in [p for p in T if PosToSymbolMap[p] == a]:
                    U = U.union(FollowposMap[pos])
                if bool(U) and frozenset(U) not in Dstates:
                    Dstates[frozenset(U)] = False
                if T not in Dtran:
                    Dtran[T] = dict()
                Dtran[T][a] = U

        self.states = list(Dstates.keys())
        pos_of_last_symbol = list(PosToSymbolMap.keys())[list(PosToSymbolMap.values()).index("#")]
        self.finite_states = [state for state in self.states if pos_of_last_symbol in state]
        self.transformation_table = Dtran

    # Каждый класс R текущего разбиения разбиваются на 2 подкласса (один из которых может быть пустым).
    # Первый состоит из состояний, которые по символу a переходят в сплиттер (R1), а второй из всех оставшихся (R2)
    def split(self, R, C, a):
        R1 = set([state for state in R if self.transformation_table[state][a] in C])
        R2 = R - R1

        return R1, R2

    def make_minimized_transformation_table(self):
        if len(self.states) == len(self.minimized_states):
            pass

    # алгоритм Хопкрофта
    def minimize(self):
        F = set(self.finite_states)
        Q_without_F = set(self.states) - set(self.finite_states)
        P = [F, Q_without_F]
        S = []
        for c in self.alphabet:
            S.append((F, c))
            S.append((Q_without_F, c))

        while S:
            splitter, symbol = S.pop()
            for R in P:
                R1, R2 = self.split(R, splitter, symbol)
                if bool(R1) and bool(R2):
                    P.remove(R)
                    P.append(R1)
                    P.append(R2)
                    if (R, symbol) in S:
                        S.remove((R, symbol))
                        S.append((R1, symbol))
                        S.append((R2, symbol))
                    elif len(R1) <= len(R2):
                        S.append((R1, symbol))
                    else:
                        S.append((R2, symbol))

        self.minimized_states = P
#        for set_with_sets in P:
#            inside_s = set()
#            for s in set_with_sets:
#                assert len(s) == 1, "Smth went wrong..."
#                inside_s.add(list(s)[0])
#            self.minimized_states.add(frozenset(inside_s))

        # self.make_minimized_transformation_table()

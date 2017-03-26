__author__ = 'alex'

# Вариант 20 % 8 = 4:
# Устранение цепных правил.
# Определение. Правила вида A -> B, где A из N и B из N, будем называть цепными.
# Постройте программу, которая в качестве входа принимает произвольную КС-грамматику G без
# eps-правил и преобразует ее в эквивалентную КС-грамматику G' без eps-правил и без цепных правил.
# Указания. Воспользоваться алгоритмом 2.11. [1]. При тестировании воспользоваться примером 2.24. [1].

import sys
import grammar_io


def is_chain(alpha, nts):
    return len(alpha) == 1 and alpha[0] in nts


def eliminate_chain_rules(grammar):
    betas = {}
    nts = sorted(grammar)

    # step 1
    for A_i in nts:
        N_prev = A_i
        i = 1
        finish = False
        while not finish:
            N_i = set().union(N_prev)
            for B in N_prev:
                for C in grammar[B]:
                    if len(C) == 1 and C[0] in nts:
                        N_i.add(C[0])
            if N_i != N_prev:
                N_prev = N_i
                i += 1
            else:
                betas[A_i] = N_i
                finish = True

    # step 2
    new_grammar = {}
    for B, alphas in grammar.items():
        for alpha in alphas:
            if not is_chain(alpha, nts):
                for A, Bs in betas.items():
                    if B in Bs:
                        if A in new_grammar:
                            new_grammar[A].add(alpha)
                        else:
                            new_grammar[A] = {alpha}

    return new_grammar


grammar = grammar_io.read(sys.stdin)

print('Original:')
grammar_io.write(grammar, sys.stdout)
print()

print('Without chain rules:')
grammar_io.write(eliminate_chain_rules(grammar), sys.stdout)
print()


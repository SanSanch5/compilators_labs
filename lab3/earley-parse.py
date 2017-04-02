__author__ = 'alex'

import sys
from grammar_io import *


class ParseError(Exception):
    pass


dot = '•'
extra_state = 'S`'


def init(words):
    return [set() for _ in words]


def finished(state):
    (_, production), _ = state
    return production[-1] == dot


def next_element(state):
    (_, production), _ = state
    return production[production.index(dot) + 1]


def predictor(state, k, G, I, log):
    B = next_element(state)
    for production in G[B]:
        new_prod = list(production)
        new_prod.insert(0, dot)
        I[k].add(((B, tuple(new_prod)), k))
        log.append('predict')


def scanner(state, k, words, I, log):
    (A, production), j = state
    ind = production.index(dot)
    a = production[ind + 1]
    if a == words[k]:
        new_prod = list(production)
        del new_prod[ind]
        new_prod.insert(ind+1, dot)
        I[k+1].add(((A, tuple(new_prod)), j))
        log.append('scan')


def completer(state, k, I, log):
    # procedure COMPLETER((B → γ•, x), k)
    # for each (A → α•Bβ, j) in S[x] do
    #     ADD-TO-SET((A → αB•β, j), S[k])
    # end
    (B, _), x = state
    for item in S[x]:
        (A, prod), j = item
        if (dot, B) in prod:
            ind = prod.index(dot)
            new_prod = list(prod)
            del new_prod[ind]
            new_prod.insert(ind+1, dot)
            I[k].add(((A, tuple(new_prod)), j))
            log.append('complete')


def earley_parse(G, initial, w):
    log = []
    nts = G.keys()

    I = init(w)

    I[0].add(((extra_state, (dot, initial)), 0))
    log.append('start rule')

    for k in range(0, len(w)):
        for state in I[k]:
            if not finished(state):
                if next_element(state) in nts:
                    predictor(state, k, G, I, log)
                else:
                    scanner(state, k, w, I, log)
            else:
                completer(state, k, I, log)

    return I, log


file = "example2.grammar"
with open(file) as grammar:
    G, initial = read(grammar)

print('Grammar wit initial state %s:' % initial)
write(G, sys.stdout)


for line in sys.stdin:
    w = line.split()
    print()
    print('Tokens:')
    print('  ', ' '.join(w))
    try:
        result, log = earley_parse(G, initial, w)
    except ParseError:
        print('SyntaxError.')
        continue

    # print result

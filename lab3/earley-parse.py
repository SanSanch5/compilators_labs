__author__ = 'alex'

import sys
from grammar_io import *


class ParseError(Exception):
    pass


dot = '•'
extra_state = 'S`'


def init(words):
    I = [[] for _ in range(0, len(words) + 1)]
    log = [[] for _ in range(0, len(words) + 1)]
    return I, log


def finished(state):
    (_, production), _ = state
    return production[-1] == dot


def next_element(state):
    (_, production), _ = state
    return production[production.index(dot) + 1]


def predictor(state, k, G, I, log, i):
    B = next_element(state)
    for production in G[B]:
        new_prod = list(production)
        new_prod.insert(0, dot)
        new_state = ((B, tuple(new_prod)), k)
        if new_state not in I[k]:
            I[k].append(new_state)
        log[k].append('predict from (%i)' % i)


def scanner(state, k, words, I, log):
    (A, production), j = state
    ind = production.index(dot)
    a = production[ind + 1]
    if a == words[k]:
        new_prod = list(production)
        del new_prod[ind]
        new_prod.insert(ind+1, dot)
        new_state = ((A, tuple(new_prod)), j)
        if new_state not in I[k+1]:
            I[k+1].append(new_state)
        log[k+1].append('scan from S(%i)(%i)' % (k, list(I[k]).index(state)))


def contains(subseq, inseq):
    return any(inseq[pos:pos + len(subseq)] == subseq for pos in range(0, len(inseq) - len(subseq) + 1))


def completer(state, k, I, log, i):
    # procedure COMPLETER((B → γ•, x), k)
    # for each (A → α•Bβ, j) in S[x] do
    #     ADD-TO-SET((A → αB•β, j), S[k])
    # end
    (B, _), x = state
    for item in I[x]:
        (A, prod), j = item
        if contains([dot, B], list(prod)):
            ind = prod.index(dot)
            new_prod = list(prod)
            del new_prod[ind]
            new_prod.insert(ind+1, dot)
            new_state = ((A, tuple(new_prod)), j)
            if new_state not in I[k]:
                I[k].append(new_state)

            # maybe error in calculating indexes for log
            log[k].append('complete from (%i) and S(%i)(%i)' % (i, x, list(I[x]).index(item)))


def earley_parse(G, initial, w):
    nts = G.keys()

    I, log = init(w)

    I[0].append(((extra_state, (dot, initial)), 0))
    log.append('start rule')

    for k in range(0, len(w) + 1):
        i = 0
        while i < len(I[k]):
            state = list(I[k])[i]
            if not finished(state):
                if next_element(state) in nts:
                    predictor(state, k, G, I, log, i)
                elif k < len(w):
                    scanner(state, k, w, I, log)
            else:
                completer(state, k, I, log, i)
            i += 1

    return I, log


file = "G5.grammar"
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
    for k, items in enumerate(result):
        input_with_dot = w.copy()
        input_with_dot.insert(k, dot)
        print("\nS(%i): " % k, ' '.join(input_with_dot))
        nt_prod = [(nt, ' '.join(product)) for (nt, product), _ in items]
        ntw, prw = map(lambda s: max(map(len, s)), zip(*nt_prod))
        for j, item in enumerate(items):
            (nt, prod), x = item
            print(("\t(%i)" % j).ljust(5), "%s -> %s" % (nt.rjust(ntw), ' '.join(prod).ljust(prw)), ("(%i)" % x).ljust(5),
                  " # %s" % log[k][j])

__author__ = 'alex'

import simplejson


with open('right-linear.json') as data_file:
    grammar = simplejson.load(data_file)


# правило формата S -> 0A | 1S | e
def preprocess_rule(rule):
    s = str(rule).replace(' ', '')
    parts = s.split('->')
    left = parts[0]
    right = parts[1].replace('|', '+')
    return left, right


def preprocess_rules(rs):
    for r in rs:
        yield preprocess_rule(r)


def paren(s):
    return '({0})'.format(s)


#  возвращает alpha*beta
def process_rule(r):
    left = str(r[0])
    right = r[1]
    parts = str(right).split('+')
    alpha_part = [p for p in parts if left in p]
    ap = []
    for alp in alpha_part:
        parts.remove(alp)
        ap.append(alp.replace(left, ''))

    alpha = '|'.join(ap)
    if len(ap) > 1:
        alpha = paren(alpha)

    beta = '+'.join(parts)
    replacement = '+'.join('{0}*{1}'.format(alpha, p) for p in parts).replace('*e', '*')

    return alpha, beta, replacement


def replace(r, start, end):
    replacement = r[1]
    parts = str(replacement).split('+')
    for i in range(start, end, 1):
        iparts = rules[i][1].split('+')
        left = r[0]
        alpha_part = [p for p in iparts if left in p]
        for alp in alpha_part:
            iparts.remove(alp)
            alp = alp.replace(left, '')
            alp = '+'.join('{0}{1}'.format(alp, p) for p in parts)
            iparts.append(alp)
        rules[i][1] = '+'.join(iparts)


def process_rules():
    n = len(rules)
    i = 1
    while i <= n:
        alpha, beta, replacement = process_rule(rules[i-1])
        rules[i-1][1] = '{0}{1}+{2}'.format(alpha, rules[i-1][0], beta)
        replace([rules[i-1][0], replacement], i, n)
        print(rules)
        i += 1
    i -= 1
    while i >= 1:
        alpha, beta, rules[i-1][1] = process_rule(rules[i-1])
        replace(rules[i-1], 0, i-1)
        print(rules)
        i -= 1
    for r in rules:
        r[1] = r[1].replace('|', '+')


rules = [[left, right] for left, right in preprocess_rules(grammar['P'])]
print(rules)
process_rules()
print(rules)


from itertools import chain


precedence = {op: p for p, ops in enumerate(reversed([
    {'**', 'abs', 'not'},
    {'*', '/', 'mod', 'rem'},
    {'+\'', '-\''},
    {'+"', '-"', '&'},
    {'<', '<=', '=', '/>', '>', '>='},
    {'and', 'or', 'xor'},
])) for op in ops}

prefix = {
    'abs', 'not',
    '+\'', '-\'',
}

variables = {chr(i) for i in range(ord('a'), ord('z') + 1)}
constants = {chr(i) for i in range(ord('0'), ord('9') + 1)}

right_associative = {'**'}

all_tokens = set(precedence) | variables | constants | {'(', ')', '$'}
relation = {t: {t: None for t in all_tokens} for t in all_tokens}

relation['('][')'] = '='

relation['$']['('] = relation['(']['('] = '<'
relation[')']['$'] = relation[')'][')'] = '>'

for thing in variables | constants:
    relation['$'][thing] = relation['('][thing] = '<'
    relation[thing]['$'] = relation[thing][')'] = '>'

for op in precedence:
    relation[op]['$'] = '>'
    relation['$'][op] = '<'

    relation[op]['('] = relation['('][op] = '<'
    relation[op][')'] = relation[')'][op] = '>'

    for thing in variables | constants:
        relation[op][thing] = '<'
        relation[thing][op] = '>'

    if op in prefix:
        for op2 in precedence:
            relation[op2][op] = '<'
            if precedence[op] > precedence[op2]:
                relation[op][op2] = '>'
            else:
                relation[op][op2] = '<'
    else:
        for op2 in precedence:
            if precedence[op] < precedence[op2] or precedence[op] == precedence[op2] \
                    and op in right_associative and op2 in right_associative:
                relation[op][op2] = '<'
                continue
            if precedence[op] > precedence[op2] or precedence[op] == precedence[op2] \
                    and op not in right_associative and op2 not in right_associative:
                relation[op][op2] = '>'
                continue


class ParseError(Exception):
    pass


def parse(tokens):
    tokens = enumerate(chain(tokens, ['$']))

    next_token_no, next_token = next(tokens)
    stack_tail, stack_head = [], '$'
    while True:
        if next_token in all_tokens:
            if stack_head == '$' and next_token == '$':
                break
            current_relation = relation[stack_head][next_token]
            if current_relation in ('<', '='):
                stack_tail.append(stack_head)
                stack_head = next_token
                next_token_no, next_token = next(tokens)
                continue
            if current_relation == '>':
                while True:
                    if stack_head not in ('(', ')'):
                        yield stack_head
                    old_stack_head = stack_head
                    stack_head = stack_tail.pop()
                    if relation[stack_head][old_stack_head] == '<':
                        break
                continue
        raise ParseError(next_token_no)


try:
    while True:
        tokens = input('> ').strip().split()
        try:
            print(' ', *parse(tokens))
        except ParseError as e:
            print('Syntax error at token #{}'.format(e.args[0]))
except EOFError:
    pass


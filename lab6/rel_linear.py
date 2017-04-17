import networkx as nx
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
            if precedence[op] < precedence[op2] or precedence[op] == precedence[op2] and op in right_associative and op2 in right_associative:
                relation[op][op2] = '<'
                continue
            if precedence[op] > precedence[op2] or precedence[op] == precedence[op2] and op not in right_associative and op2 not in right_associative:
                relation[op][op2] = '>'
                continue

graph = nx.DiGraph()
n = 0
for t in relation:
    graph.add_node(n, {'bases': {('f', t)}})
    n += 1
    graph.add_node(n, {'bases': {('g', t)}})
    n += 1


def find_node(graph, base):
    for n, n_data in graph.nodes(data=True):
        if base in n_data['bases']:
            return n
    raise ValueError()

for t1 in relation:
    n1 = find_node(graph, ('f', t1))
    for t2 in relation:
        n2 = find_node(graph, ('g', t2))
        if relation[t1][t2] == '=':
            graph.add_edge(n1, n2, {'merge': None})
            graph.add_edge(n2, n1, {'merge': None})
        elif relation[t1][t2] == '>':
            graph.add_edge(n1, n2)
        elif relation[t1][t2] == '<':
            graph.add_edge(n2, n1)

while True:
    old_n = n
    for a, a_data in graph.nodes(data=True):
        if n != old_n:
            break
        for b, b_data in graph.nodes(data=True):
            if a == b:
                continue
            if not graph.has_edge(a, b):
                continue
            if 'merge' not in graph.get_edge_data(a, b):
                continue
            graph.add_node(n, {'bases': a_data['bases'] | b_data['bases']})
            for i in graph.predecessors(a):
                graph.add_edge(i, n, graph.get_edge_data(i, a))
            for i in graph.predecessors(b):
                graph.add_edge(i, n, graph.get_edge_data(i, b))
            for o in graph.successors(a):
                graph.add_edge(n, o, graph.get_edge_data(a, o))
            for o in graph.successors(b):
                graph.add_edge(n, o, graph.get_edge_data(b, o))
            n += 1
            graph.remove_node(a)
            graph.remove_node(b)
            break

    if n == old_n:
        break

for n in graph.nodes():
    if graph.has_edge(n, n):
        graph.remove_edge(n, n)

graph2 = graph.copy()
while True:
    if not graph2.nodes():
        break
    for n in graph2.nodes():
        if not graph2.successors(n):
            graph2.remove_node(n)
            break
    else:
        raise ValueError('Relation graph has cycles')

longest_paths_from = {n: 0 for n in graph.nodes()}
while True:
    old_longest_paths_from = longest_paths_from.copy()
    for n in graph.nodes():
        longest_paths_from[n] = 0
        for n2 in graph.successors(n):
            longest_paths_from[n] = max(longest_paths_from[n], 1 + longest_paths_from[n2]) 
    if longest_paths_from == old_longest_paths_from:
        break

f = {t: longest_paths_from[find_node(graph, ('f', t))] for t in relation}
g = {t: longest_paths_from[find_node(graph, ('g', t))] for t in relation}


class ParseError(Exception):
    pass


def parse(tokens):
    tokens = enumerate(chain(tokens, ['$']))

    next_token_no, next_token = next(tokens)
    stack_tail, stack_head = [], '$'
    while True:
        if next_token not in all_tokens:
            raise ParseError(next_token_no)
        if stack_head == '$' and next_token == '$':
            break
        if f[stack_head] <= g[next_token]:
            stack_tail.append(stack_head)
            stack_head = next_token
            next_token_no, next_token = next(tokens)
        else:
            while True:
                if stack_head not in ('(', ')'):
                    yield stack_head
                old_stack_head = stack_head
                stack_head = stack_tail.pop()
                if f[stack_head] < g[old_stack_head]:
                    break


try:
    while True:
        tokens = input('> ').strip().split()
        try:
            print(' ', *parse(tokens))
        except ParseError as e:
            print('Syntax error at token #{}'.format(e.args[0]))
except EOFError:
    pass


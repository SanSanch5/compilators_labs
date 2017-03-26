def read(stream):
    grammar = {}
    for line in stream:
        line = line.strip()
        if not line:
            continue

        lhs, rhs = line.split('->')
        lhs = lhs.strip()
        rhs = rhs.strip()
        rhs = tuple(rhs.split())

        if lhs in grammar:
            grammar[lhs].add(rhs)
        else:
            grammar[lhs] = {rhs}

    return grammar


def write(grammar, stream):
    for lhs in sorted(grammar):
        for rhs in sorted(grammar[lhs]):
            print(lhs, '->', *rhs, file=stream)


#!/usr/bin/env python

import readline


def parse(tokens):
    def t(p):
        if p < len(tokens):
            return tokens[p]
        return None

    class ParseError(Exception):
        pass

    def err(p):
        raise ParseError(p)

    def program(p):
        p = block(p)
        return p

    def block(p):
        if t(p) == '{':
            p += 1
            p = statement_list(p)
            if t(p) == '}':
                p += 1
                return p
            err(p)
        err(p)

    def statement_list(p):
        def tail(p):
            if t(p) == ';':
                p += 1
                p = statement_list(p)
            return p

        p = statement(p)
        p = tail(p)
        return p

    def statement(p):
        if t(p) == 'a':
            p += 1
            if t(p) == '=':
                p += 1
                p = expression(p)
                return p
            err(p)
        else:
            p = block(p)
            return p
        err(p)

    def expression(p):
        def logical(p):
            p = relational(p)
            if t(p) in ('and', 'or', 'xor'):
                p += 1
                p = relational(p)
            return p

        def relational(p):
            p = simple(p)
            if t(p) in ('<', '<=', '==', '/>', '>=', '>'):
                p += 1
                p = simple(p)
            return p

        def simple(p):
            if t(p) in ('+', '-'):
                p += 1
            p = term(p)
            if t(p) in ('+', '-', '&'):
                p += 1
                p = term(p)
            return p

        def term(p):
            p = factor(p)
            if t(p) in ('*', '/', 'mod', 'rem'):
                p += 1
                p = factor(p)
            return p

        def factor(p):
            if t(p) in ('abs', 'not'):
                p += 1
            p = primary(p)
            if t(p) == '**':
                p += 1
                p = primary(p)
            return p

        def primary(p):
            if t(p) in ('0', 'a'):
                p += 1
                return p
            elif t(p) == '(':
                p += 1
                p = logical(p)
                if t(p) == ')':
                    p += 1
                    return p
                err(p)
            err(p)

        p = logical(p)
        return p

    try:
        p = 0
        p = program(p)
        if p == len(tokens):
            return None
        return p
    except ParseError as e:
        return e.args[0]

try:
    while True:
        tokens = input('> ').strip().split()
        error = parse(tokens)
        if error is None:
            print('Ok')
            continue
        print('Syntax error on token #{}'.format(error))
except EOFError:
    pass


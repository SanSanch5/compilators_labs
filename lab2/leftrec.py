# Устранение левой рекурсии.
# Постройте программу, которая в качестве входа принимает приведенную КС-грамматику G и
# преобразует ее в эквивалентную КС-грамматику G' без левой рекурсии.
# Указания.
# 1) Проработать самостоятельно п. 4.3.3. и п. 4.3.4. [2].
# 2) Воспользоваться алгоритмом 2.13. При тестировании воспользоваться примером 2.27. [1].
# 3) Воспользоваться алгоритмами 4.8 и 4.10. При тестировании воспользоваться примерами 4.7., 4.9. и
# 4.11. [2].
# 4) Устранять надо не только непосредственную (immediate), но и косвенную (indirect) рекурсию. Этот
# вопрос подробно затронут в [4].
# 5) После устранения левой рекурсии можно применить левую факторизацию.


import sys
import grammar_io


def eliminate_left_recursion(grammar):
    nts = sorted(grammar)
    for A_i in nts:
        for A_j in nts:
            if A_j == A_i:
                break

            for rhs in grammar[A_i].copy():
                if not rhs or rhs[0] != A_j:
                    continue
                gamma = rhs[1:]

                grammar[A_i].remove((A_j,) + gamma)
                for sigma in grammar[A_j]:
                    grammar[A_i].add(sigma + gamma)

        grammar[A_i + '`'] = {()}
        for alpha_i in grammar[A_i].copy():
            grammar[A_i].remove(alpha_i)
            if alpha_i and alpha_i[0] == A_i:
                grammar[A_i + '`'].add(alpha_i[1:] + (A_i + '`',))
            else:
                grammar[A_i].add(alpha_i + (A_i + '`',))

    return grammar

grammar = grammar_io.read(sys.stdin)

print('Original:')
grammar_io.write(grammar, sys.stdout)
print()

print('Without left recursion:')
grammar_io.write(eliminate_left_recursion(grammar), sys.stdout)
print()


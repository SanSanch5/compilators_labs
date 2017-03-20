__author__ = 'alex'

# Напишите программу, которая в качестве входа принимает произвольное регулярное выражение, и выполняет
# следующие преобразования:
# 1) Преобразует регулярное выражение непосредственно в ДКА.
# 2) По ДКА строит эквивалентный ему КА, имеющий наименьшее возможное количество состояний.
# Указание. Воспользоваться алгоритмом, приведенным по адресу
# http://neerc.ifmo.ru/wiki/index.php?title=Минимизация_ДКА,_алгоритм_Хопкрофта_(сложность_O(n_log_n)
# )
# 3) Моделирует минимальный КА для входной цепочки из терминалов исходной грамматики.


from dfa import DFA


regexp = "(a|b)*abb"
dfa = DFA()
dfa.make(regexp)
print('DFA:')
print('Alphabet: ', dfa.alphabet)
print('Start', dfa.start_state)
print('States', dfa.states)
print('Transformation table', dfa.transformation_table)
print('Finite states', dfa.finite_states)

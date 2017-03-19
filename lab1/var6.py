__author__ = 'alex'

# Напишите программу, которая в качестве входа принимает произвольное регулярное выражение, и выполняет
# следующие преобразования:
# 1) Преобразует регулярное выражение непосредственно в ДКА.
# 2) По ДКА строит эквивалентный ему КА, имеющий наименьшее возможное количество состояний.
# Указание. Воспользоваться алгоритмом, приведенным по адресу
# http://neerc.ifmo.ru/wiki/index.php?title=Минимизация_ДКА,_алгоритм_Хопкрофта_(сложность_O(n_log_n)
# )
# 3) Моделирует минимальный КА для входной цепочки из терминалов исходной грамматики.


from dfa_maker import make_dfa


regexp = "(a|b)*abb"
alphabet, start, states, transform_table, finite = make_dfa(regexp)
print('Alphabet: ', alphabet)
print('Start', start)
print('States', states)
print('Transformation table', transform_table)
print('Finite states', finite)

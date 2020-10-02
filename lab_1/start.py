"""
Concordance implementation starter
"""

from main import *
import os


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))

    #  here goes your logic: calling methods from concordance.py
    tokens = tokenize(data) # токенезирование
    stop_words = get_stop_words()
    # токены без стоп слов
    tokens_clean = remove_stop_words(tokens, stop_words)
    # частоты токенов
    freq_dict = calculate_frequencies(tokens_clean)
    # слово для поиска
    word = input()
    left_size, right_size = int(input()), int(input())

    result_normal_concordance = get_concordance(tokens_clean, word, left_size, right_size)
    result_adjacent_concordance = get_adjacent_words(tokens, word, left_size, right_size)
    result_sorted_concordance = sort_concordance(tokens, word, left_size, right_size, True)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'

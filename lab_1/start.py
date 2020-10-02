"""
Concordance implementation starter
"""

import os
import main

from random import choice
preview_length = 3

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('tokenize:', tokens[:preview_length * 10], "\n")

    token_frequency = main.calculate_frequencies(tokens[:preview_length * 10])
    print('frequency of tokens:', token_frequency, "\n")

    random_word = choice(tokens)

    concordance = main.get_concordance(tokens, random_word, 3, 2)
    print('concordance of word "{}":'.format(random_word), concordance, "\n")

    adjacent = main.get_adjacent_words(tokens, random_word, 3, 2)
    print('adjacent words for "{}"'.format(random_word), adjacent, "\n")

    sorted_concordance = main.sort_concordance(tokens, random_word, 3, 2, False)
    print('sorted concordance for "{}", left_sort=False'.format(random_word), sorted_concordance, "\n")

    main.write_to_file('report.txt', sorted_concordance)


    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    RESULT = sorted_concordance
    assert RESULT, 'Concordance not working'

"""
Concordance implementation starter
"""

import os
import main

if __name__ == '__main__':
    #  here goes your logic: calling methods from concordance.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    tokens = main.tokenize(data)
    print('tokenize', tokens[:10])

    tokens = main.remove_stop_words(tokens, stop_words)
    print('remove_stop_words', tokens[:10])

    frequencies = main.calculate_frequencies(tokens[:5000])
    print('calculate_frequencies', frequencies[tokens[0]])

    concordance = main.get_concordance(tokens, 'name', 3, 0)
    print('get_concordance', concordance[:5])

    adjacent = main.get_adjacent_words(tokens, 'dog', 2, 0)
    print('get_adjacent_words', adjacent[:5])

    sorted_concordance = main.sort_concordance(tokens, 'cat', 5, 2, True)
    print('sort_concordance', sorted_concordance[:5])

    RESULT = sorted_concordance
    assert RESULT, 'Concordance not working'

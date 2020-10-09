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

    #  use data.txt file to test your program
    tokens = main.tokenize(data)
    print('tokenize', tokens[:4])

    tokens = main.remove_stop_words(tokens, stop_words)
    print('remove_stop_words', tokens[:4])

    frequencies = main.calculate_frequencies(tokens[:5000])
    print('calculate_frequencies', frequencies[tokens[0]])

    concordance = main.get_concordance(tokens, 'happy', 3, 0)
    print('get_concordance', concordance[:4])

    adjacent = main.get_adjacent_words(tokens, 'happy', 3, 0)
    print('get_adjacent_words', adjacent[:4])

    sorted_concordance = main.sort_concordance(tokens, 'happy', 3, 0, True)
    print('sort_concordance', sorted_concordance[:4])

    main.write_to_file('report.txt', sorted_concordance)

    RESULT = sorted_concordance
    assert RESULT, 'Concordance not working'

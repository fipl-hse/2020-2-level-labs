"""
Concordance implementation starter
"""

import os
import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    stop_words = stop_words.split()

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print(tokens[:30])

    tokens_clear = main.remove_stop_words(tokens, stop_words)
    print(tokens_clear[:30])

    freq_dict = main.calculate_frequencies(tokens[:100])
    print(freq_dict)

    top_7_words = main.get_top_n_words(freq_dict, 7)
    print(top_7_words)

    concordance = main.get_concordance(tokens,'apple', 3, 4)
    print(concordance)

    adjacent_words = main.get_adjacent_words(tokens, 'apple', 2, 3)
    print(adjacent_words)

    sorted_concordance = main.sort_concordance(tokens, 'apple', 1, 2, False)
    print(sorted_concordance)

    main.write_to_file('report.txt', sorted_concordance)

    RESULT = sorted_concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

"""
Concordance implementation starter
"""


import os
import main


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('tokenize', tokens[:5])
    tokens = main.remove_stop_words(tokens, stop_words)
    print('remove_stop_words', tokens[:5])
    frequencies = main.calculate_frequencies(tokens)
    print('calculate_frequencies', frequencies[tokens[0]])
    concordance = main.get_concordance(tokens, 'dog', 2, 0)
    print('get_concordance', concordance[:5])
    adjacent = main.get_adjacent_words(tokens, 'dog', 2, 0)
    print('get_adjacent_words', adjacent[:5])
    sorted_concordance = main.sort_concordance(tokens, 'dog', 2, 0, True)
    print('sort_concordance', sorted_concordance[:5])
    main.write_to_file('', sorted_concordance)
    check = (all(isinstance(s, list) for s in sorted_concordance))
    RESULT = isinstance(sorted_concordance, list) and check
    #  DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

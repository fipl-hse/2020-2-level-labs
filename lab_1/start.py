"""
Concordance implementation starter
"""

import os
from lab_1 import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    stop_words = stop_words.split()

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('Tokens:', tokens[:4])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST

    tokens = main.remove_stop_words(tokens, stop_words)
    print('Tokens without stop words:', tokens[:4])

    tokens_frequencies = main.calculate_frequencies(tokens[:5000])
    print('The frequency dictionary of tokens is:', tokens[:10])

    top_n_words = main.get_top_n_words(tokens_frequencies, 20)
    print('Top 20 words:', top_n_words)

    concordance = main.get_concordance(tokens, 'team', 3, 0)
    print("The concordance for word 'task':", concordance[:4])

    adjacent = main.get_adjacent_words(tokens, 'team', 3, 0)
    print("The adjacent for word 'task': ", adjacent[:4])

    main.write_to_file('tokens.txt', top_n_words)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    RESULT = tokens
    assert RESULT == [['years', 'of', 'time', 'team'],
                      ['presented', 'a', 'round', 'up'],
                      ['of', 'what', 'has', 'happened' 'in']], 'Concordance not working'

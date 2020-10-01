"""
Concordance implementation starter
"""

import os
from lab_1 import main
from lab_1.main import read_from_file

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file(os.path.join(current_dir, 'stop_words.txt')).split()

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('Tokens:', tokens[:20])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    tokens_stop_words = main.remove_stop_words(tokens, stop_words)
    print('Tokens without stop words:', tokens_stop_words[:20])

    tokens = main.remove_stop_words(tokens, stop_words)
    print('Tokens without stop words:', tokens[:10])

    tokens_frequencies = main.calculate_frequencies(tokens_stop_words[:20])
    print('The frequency dictionary of tokens is:', tokens[:10])

    top_n_words = main.get_top_n_words(tokens_frequencies, 20)
    print('Top 20 words:', top_n_words)

    concordance = main.get_concordance(tokens, 'task', 2, 3)
    print("The concordance for word 'task':", concordance[:6])

    adjacent = main.get_adjacent_words(tokens, 'task', 2, 3)
    print("The adjacent for word 'task': ", adjacent)

    main.write_to_file('report.txt', top_n_words)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    RESULT = top_n_words
    assert RESULT, 'Concordance not working'

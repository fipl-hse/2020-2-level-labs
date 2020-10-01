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
    stop_words = read_from_file(os.path.join(current_dir, 'stop_words.txt'))

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print(tokens[:10])

    RESULT = None
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    tokens = main.remove_stop_words(tokens[:6], [stop_words])
    print('Stop words have been removed: {}'. format(tokens))

    freq_dict = main.calculate_frequencies(tokens)
    print('The frequency dictionary of tokens is: {}'. format(freq_dict))

    top_n_words = main.get_top_n_words(freq_dict, 2)
    print('Top_n_words:'. format(top_n_words)

    concordance = main.get_concordance(tokens, 'division', 2, 3)
    print('The concordance for the token "division" is: {}'. format(concordance))

    adjacent = main.get_adjacent_words(tokens, 'team', 2, 2)
    print('The adjacent words is: '. format(adjacent)

    assert RESULT == [(), ()], 'Concordance not working'
    assert RESULT == [['of', 'a']], 'Concordance not working'

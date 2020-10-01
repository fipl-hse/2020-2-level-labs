"""
Concordance implementation starter
"""

import main
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    text = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    stop_words = stop_words.split('\n')

    #  here goes your logic: calling methods from concordance.py

    tokens = main.tokenize(text)
    print('Tokens: ', tokens[:20])

    tokens = main.remove_stop_words(tokens, stop_words)
    print('Tokens without stop words: ', tokens[:20])

    freq_dict = main.calculate_frequencies(tokens)
    print('Frequency for the first word: ', freq_dict[tokens[0]])

    top_list = main.get_top_n_words(frequencies, 3)
    print('Top 3 words: ', top_list)

    concordance = main.get_concordance(tokens, 'time', 2, 3)
    print('Concordance for "time":', concordance)

    adjacent_words = main.get_adjacent_words(tokens, 'time', 2, 3)
    print ('Adjacent words for "time":', adjacent_words)

    RESULT = adjacent_words

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'

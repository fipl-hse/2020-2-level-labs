"""
Concordance implementation starter
"""

import os
import main
from lab_1.main import read_from_file
if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('tokens: ', tokens[:5])

    stop_words = main.remove_stop_words(tokens, stop_words)
    print('without stop words: ', tokens[:5])

    frequencies = main.calculate_frequencies(tokens)
    print('frequency for a word:', frequencies[tokens[5]])

    top_n = main.get_top_n_words(frequencies, 10)
    print('top 10 words: ', top_n)

    concordance = main.get_concordance(tokens, 'sunny', 2, 3)
    print('concordance for the word: ', concordance[:3])

    adjacent_words = main.get_adjacent_words(tokens, 'sunny', 2, 3)
    print('adjacent_words for the word: ', adjacent_words[:3])

    main.write_to_file('report.txt', adjacent_words)

    RESULT = adjacent_words
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

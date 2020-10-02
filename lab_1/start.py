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

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('tokens: ', tokens[:6])

    stop_words = main.remove_stop_words(tokens,stop_words)
    print("stop_words:", tokens[:6])

    frequencies = main.calculate_frequencies(tokens)
    print('frequencies for the word: ', frequencies[tokens[2]])

    top_n = main.get_top_n_words(frequencies,10)
    print('top of 10 words: ', top_n)

    concordance = main.get_concordance(tokens, 'people', 2, 3)
    print('concordance for the word: ', concordance[:6])

    adjacent_words = main.get_adjacent_words (tokens, 'people',2, 2)
    print('adjacent words for the word: ', adjacent_words[:3])

    write_file = ('report.txt', adjacent_words)

    RESULT = adjacent_words[:3]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [[['presented', 'in', 'people', 'who', 'wereare'], ['it', 'but', 'people', 'like', 'the']],\
    [['presented', 'in', 'people', 'who', 'wereare'], ['it', 'but', 'people', 'like', 'the']],\
    [['presented', 'in', 'people', 'who', 'wereare'], ['it', 'but', 'people', 'like', 'the']]],\
    'Concordance not working'

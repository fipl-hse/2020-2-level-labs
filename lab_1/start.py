"""
Concordance implementation starter
"""
import os
import main
from main import read_from_file


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt')).split('\n')

    tokens = main.tokenize(data)
    print('tokens', tokens[:5])

    tokens = main.remove_stop_words(tokens, stop_words)
    print('tokens without stop words', tokens[:5])

    frequency = main.calculate_frequencies(tokens)
    print('frequency for the fifth word', frequency[tokens[4]])

    top_5 = main.get_top_n_words(frequency, 5)
    print('top five words', top_5)

    concordance_moose = main.get_concordance(tokens, 'moose', 1, 4)
    print('concordance for "moose"', concordance_moose[:5])

    #  here goes your logic: calling methods from concordance.py

    RESULT = frequency
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

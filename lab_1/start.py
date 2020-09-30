"""
Concordance implementation starter
"""

from main import read_from_file
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import get_concordance
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    text = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file((os.path.join(current_dir, 'stop_words.txt')))
    stop_words = stop_words.split('\n')

    #  here goes your logic: calling methods from concordance.py
    tokens = tokenize(text) [:101]
    print ('The first 100 tokens are: {}'. format(tokens))

    tokens = remove_stop_words(tokens, stop_words)
    print('Stop words have been removed: {}'.format(tokens))

    freq_dict = calculate_frequencies(tokens)
    print ('The frequency dictionary of tokens is: {}'. format(freq_dict))

    top_words = get_top_n_words(freq_dict, 3)
    print('There are three the most popular words: {}'. format(top_words))

    concordance = get_concordance(tokens, 'division', 2, 3)
    print('The concordance for the token "division" is: {}'. format(concordance))

    RESULT = concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['recommended', 'a', 'division', 'main', 'services', 'relocation']], 'Concordance not working'

"""
Concordance implementation starter
"""

from main import read_from_file
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    stop_words = stop_words.split()
    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    tokens = main.remove_stop_words(tokens,stop_words)
    freq_dict = main.calculate_frequencies(tokens)
    top_n_tokens = main.get_top_n_words(freq_dict, 2)
    concordance = main.get_concordance(tokens, 'seriously', 1, 1)
    adjacent_words = main.get_adjacent_words(tokens, 'seriously', 1, 1)

    RESULT = adjacent_words
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

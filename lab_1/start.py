"""
Concordance implementation starter
"""

from main import *
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file(os.path.join(current_dir, 'stop_words.txt')).split()
    tokens = tokenize(data)
    tokens_no_stop_words = remove_stop_words(tokens, stop_words)
    tokens_freq = calculate_frequencies(tokens_no_stop_words)
    n_words = 10
    top_n_words = get_top_n_words(tokens_freq, n_words)
    print('top', n, 'words:', top_n_words)
    concordance = get_concordance(tokens, 'point', 2, 2)
    print('concordance of the word "point:"',concordance)
    adjacent_words = get_adjacent_words(tokens_no_stop_words, 'point', 2, 2)
    print('adjacent words of the word "point"', adjacent_words)
    write_to_file(os.path.join(current_dir, 'adjacent_king.txt'), adjacent_words)
    RESULT = contexts_no_stop_words
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'

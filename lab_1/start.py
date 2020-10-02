"""
Sample change by me
Concordance implementation starter
"""
import os
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import get_concordance
from main import get_adjacent_words
from main import read_from_file
from main import sort_concordance

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py
    tokens = tokenize(data)
    stop_words = read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    clean_text_list = remove_stop_words(tokens, stop_words)
    frequencies_dict = calculate_frequencies(tokens)
    top_n_words = get_top_n_words(frequencies_dict, 5)
    concordance = get_concordance(tokens, 'sodium', 2, 2)
    adjacent_words = get_adjacent_words(tokens, 'sodium', 2, 2)

    RESULT = sort_concordance(tokens, 'sodium', 1, 1, True)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['by', 'sodium', 'bicarbonate'], ['epithelial', 'sodium', 'channels'],
                      ['means', 'sodium', 'aluminate'], ['the', 'sodium', 'salt']]

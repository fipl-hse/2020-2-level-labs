"""
Sample change by me
Concordance implementation starter
"""
import os
from main import tokenize
from main import read_from_file
from main import sort_concordance


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py
    tokens = tokenize(data)


    RESULT = sort_concordance(tokens, 'sodium', 1, 1, True)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['by', 'sodium', 'bicarbonate'], ['epithelial', 'sodium', 'channels'],
                      ['means', 'sodium', 'aluminate'], ['the', 'sodium', 'salt']]

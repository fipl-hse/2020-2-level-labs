"""
Sample change by me
Concordance implementation starter
"""
from main import tokenize
from main import sort_concordance
from main import read_from_file
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'lab_1/data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py
    text = read_from_file('lab_1/data.txt')
    tokens = tokenize(text)
    RESULT = sort_concordance(tokens, 'sodium', 1, 1, True)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['by', 'sodium', 'bicarbonate'], ['epithelial', 'sodium', 'channels'],
                      ['means', 'sodium', 'aluminate'], ['the', 'sodium', 'salt']]


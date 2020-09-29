"""
Concordance implementation starter
"""

import os

from main import read_from_file, tokenize, sort_concordance

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    tokens = tokenize(data)

    #  here goes your logic: calling methods from concordance.py
    sorted_concordance = sort_concordance(tokens, 'fitness', 1, 1, True)

    RESULT = sorted_concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

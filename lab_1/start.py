"""
Concordance implementation starter
"""

import os
import main

from random import choice
preview_length = 3

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('tokenize:', tokens[:preview_length * 10], "\n")

    RESULT = None
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'

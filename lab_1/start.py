"""
Concordance implementation starter
"""

import os
import main
from main import read_from_file

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'data.txt'))

    #  here goes your logic: calling methods from concordance.py

    data_in_tok= main.tokenize (data)
    data_w_punc=main.remove_stop_words(data_in_tok,'data.txt')


    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert main.get_adjacent_words == [['man', 'is'], ['dog, 'cat']]
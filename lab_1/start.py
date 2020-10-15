"""
Concordance implementation starter
"""

import os
import main

if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    # just a shorter version of data.txt because my pc couldn't run start.py with 10000 string file...
    stop_words = (main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))).split('\n')

    #  here goes your logic: calling methods from concordance.py


    RESULT = None
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [[], []], 'Concordance not working'

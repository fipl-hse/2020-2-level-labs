"""
Concordance implementation starter
"""
import os
from main import read_from_file, sort_concordance, tokenize
if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []
    #  here goes your logic: calling methods from concordance.py
    tokens = tokenize(data)
    RESULT = sort_concordance(tokens, 'text', 1, 2, True)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT,  'sort concordance not working'
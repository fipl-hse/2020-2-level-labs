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
    res = sort_concordance(tokens, 'text', 1, 2, True)
    print(res[:3])
    RESULT = res[:2]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['80', 'text', 'columns', 'although'], ['a', 'text', 'as', 'quickly']],  'sort concordance not working'

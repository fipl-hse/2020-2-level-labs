"""
Concordance implementation starter
"""
import os
import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py

    tokens = main.tokenize(data)
    res = main.sort_concordance(tokens, 'text', 1, 2, True)
    RESULT = res[:2]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['80', 'text', 'columns', 'although'], ['a', 'text', 'as', 'quickly']],\
        'sort concordance not working'
    print(RESULT)

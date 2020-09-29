"""
Concordance implementation starter
"""

from main import read_from_file
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py
    concordance = main.get_concordance(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                                        'the', 'dog', 'is', 'glad', 'but', 'the', 'cat', 'is', 'sad'],
                                       'happy', 2, 3)
    RESULT = ['man', 'is', 'happy', 'the', 'dog', 'is']
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

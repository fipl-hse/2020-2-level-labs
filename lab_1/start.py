"""
Concordance implementation starter
"""

import os
from main import read_from_file

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py

    RESULT = tokenize ('The weather is sunny, the man is happy.')
    RESULT=remove_stop_words(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy'],['the', 'is'])
    RESULT=calculate_frequencies(['weather', 'sunny', 'man', 'happy'])
    RESULT=get_top_n_words(['weather', 'sunny', 'man', 'happy', 'and', 'dog', 'happy'],1)
    RESULT=get_concordance(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad'],'happy',2,3)
    RESULT=get_adjacent_words(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad'],'happy',2,3)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['man', 'is'], ['dog, 'cat']], 'Concordance not working'

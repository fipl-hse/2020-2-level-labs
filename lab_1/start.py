"""
Concordance implementation starter
"""

from main import *
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = [read_from_file(os.path.join(current_dir, 'data.txt'))]

    #  here goes your logic: calling methods from concordance.py
    test_text = read_from_file('text.txt')
    my_freq_dict = calculate_frequencies(tokenize(test_text))
    top = get_top_n_words(my_freq_dict, 1)
    print(top)
    print(tokenize(test_text))
    print(get_concordance(tokenize(test_text), 'amet', 3, 2))
    print(get_adjacent_words(tokenize(test_text), 'ipsum', 1, 5))

    RESULT = get_concordance(tokenize(test_text), '#g', 0, 0)
    write_to_file('result1.txt', get_concordance(tokenize(test_text), 'ex', 3, 2))

    RESULT = get_concordance(tokenize(test_text), '#g', 0, 0)
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    # assert RESULT == [(), ()], 'Concordance not working'
    assert RESULT == [], 'Concordance not working'

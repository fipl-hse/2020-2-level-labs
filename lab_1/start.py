"""
Concordance implementation starter
"""

import os
from lab_1 import main


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    stop_words = stop_words.split()
    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print(tokens)
    new_tokens = main.remove_stop_words(tokens, stop_words)
    print(new_tokens)
    freq_dict = main.calculate_frequencies(new_tokens)
    print(freq_dict)
    top_n_tokens = main.get_top_n_words(freq_dict, 2)
    print(top_n_tokens)
    concordance = main.get_concordance(new_tokens, 'cat', 1, 1)
    print(concordance)
    adjacent_words = main.get_adjacent_words(new_tokens, 'cat', 1, 1)
    print(adjacent_words)
    sort_concordance_lst = main.sort_concordance(new_tokens, 'cat', 1, 1, True)
    print(sort_concordance_lst)
    main.write_to_file('report.txt', sort_concordance_lst)
    RESULT = sort_concordance_lst
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

"""
Concordance implementation starter
"""

import os
import main


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt')).split('\n')

    #  here goes your logic: calling methods from concordance.py
    tokenized_data = main.tokenize(data)
    clean_data = main.remove_stop_words(tokenized_data, stop_words)

    top_n = main.get_top_n_words(main.calculate_frequencies(clean_data), 13)
    print(top_n[-1])

    closest_words = main.get_adjacent_words(clean_data, top_n[-1], 3, 2)
    if len(closest_words) > 0:
        print(f"Third words from the left and second words from the right for "
              f"the word {top_n[-1]} (first 5 cases) are")
        for adjacent_words in closest_words[:5]:
            print('\t', adjacent_words)

    sorted_concordance_left = main.sort_concordance(clean_data, top_n[-1], 2, 2, True)
    if len(sorted_concordance_left) > 0:
        print('Concordance sorted by the first left word (first 5 cases):')
        for concordance in sorted_concordance_left[:5]:
            print('\t', concordance)

    sorted_concordance_right = main.sort_concordance(clean_data, top_n[-1], 2, 2, False)
    if len(sorted_concordance_right) > 0:
        print('Concordance sorted by the first right word (first 5 cases):')
        for concordance in sorted_concordance_right[:5]:
            print('\t', concordance)

    RESULT = sorted_concordance_left
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT != [], 'Concordance not working'

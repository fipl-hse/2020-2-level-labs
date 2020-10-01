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

    tokens = main.tokenize(data)
    print('tonkes:', tokens[:5])

    tokens = main.remove_stop_words(tokens,stop_words)
    print('tokens without stop_words:', tokens[:5])

    freq_dict = main.calculate_frequencies(tokens)
    print('freq_dict:', freq_dict[tokens[0]])

    top_words = main.get_top_n_words(freq_dict, 1)
    print('top_words:', top_words)

    concordance = main.get_concordance(tokens, 'happy', 2, 3)
    print('concordance:', concordance[:5])

    left_right_word = main.get_adjacent_words(tokens, 'happy', 2, 3)
    print('adjacent_words:', left_right_word[:5])

    sorted_concordance = main.sort_concordance(tokens, 'happy', 2, 3, True)
    print('sorted_concordance:', sorted_concordance)

    main.write_to_file('report.txt', sorted_concordance)
    #  here goes your logic: calling methods from concordance.py

    RESULT = sorted_concordance[:5]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    #assert RESULT == [(), ()], 'Concordance not working'

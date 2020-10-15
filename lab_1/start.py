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
    tokens = main.tokenize(data)
    print('tokens:', tokens[:10])
    print('\n-----------------------------\n')

    tokens = main.remove_stop_words(tokens, stop_words)   # old: 34 sec, new - 3.4 sec
    print('tokens without stop words:', tokens[:10])
    print('\n-----------------------------\n')

    frequencies = main.calculate_frequencies(tokens)  # old: 116 sec, new: ~81 sec
    print('frequency for the first word:', frequencies[tokens[0]])
    print('\n-----------------------------\n')

    top_10 = main.get_top_n_words(frequencies, 10)
    print('top 10 words:', top_10)
    print('\n-----------------------------\n')

    concordance_cat = main.get_concordance(tokens, 'cat', 2, 3)
    print('concordance for "cat", left = 2, right = 3:', concordance_cat[:5])
    print('\n-----------------------------\n')

    adjacent_words_cat = main.get_adjacent_words(tokens, 'cat', 2, 3)
    print('adjacent words for "cat" left = 2, right = 3:', adjacent_words_cat[:5])
    print('\n-----------------------------\n')

    sorted_concordance_cat = main.sort_concordance(tokens, 'cat', 2, 3, True)
    print('sorted concordance for "cat" left = 2, right = 3:', sorted_concordance_cat[:5])
    print('\n-----------------------------\n')

    main.write_to_file('report.txt', sorted_concordance_cat)

    RESULT = sorted_concordance_cat
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

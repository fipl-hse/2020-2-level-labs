"""
Concordance implementation starter
"""


import os
import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt')).split()

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    # print('tokens:', tokens[:10], '...')

    tokens = main.remove_stop_words(tokens, stop_words)
    # print('tokens without stop words:', tokens[:10], '...')

    # frequency_dictionary = main.calculate_frequencies(tokens)
    # print('frequency of "time":', frequency_dictionary['time'])

    # top_10_words = main.get_top_n_words(frequency_dictionary, 10)
    # print('the most frequent 10 words:', top_10_words)

    # concordance = main.get_concordance(tokens, 'rocket', 2, 3)
    # print('contexts for "rocket":', concordance)

    # adjacent_words = main.get_adjacent_words(tokens, 'rocket', 2, 3)
    # print('adjacent words for "rocket":', adjacent_words)

    sorted_concordance = main.sort_concordance(tokens, 'rocket', 2, 3, False)
    # print('sorted concordance for "rocket":', sorted_concordance)

    main.write_to_file('report.txt', sorted_concordance)

    RESULT = sorted_concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['estimated', 'executed', 'rocket', 'arena', 'ability', 'players'],
                      ['limits', 'speed', 'rocket', 'maximum', 'exhaust', 'speed'],
                      ['zenitsl', 'carrier', 'rocket', 'pizza', 'restaurants', 'pizza']], 'Concordance not working'

"""
Concordance implementation starter
"""

import main
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt')).split('\n')

    
    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('tokens:', tokens[:7])

    tokens = main.remove_stop_words(tokens, stop_words)
    print('tokens without stop words', tokens[:7])

    frequency = main.calculate_frequencies(tokens)
    print('frequency for the second word:', frequencies[tokens[2]])

    top_7 = main.get_top_n_words(frequency, 7)
    print('top 7 words:', top_7)

    concordance_love = main.get_concordance(tokens, 'love', 3, 4)
    print('concordance for "love":', concordance_love[:7])

    adjacent_words_windy = main.get_adjacent_words(tokens, '', 2, 3)
    print('adjacent words for "windy":', adjacent_words_windy[:5])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

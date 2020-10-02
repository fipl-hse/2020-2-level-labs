"""
Concordance implementation starter
"""

import os

from main import calculate_frequencies
from main import get_adjacent_words
from main import get_concordance
from main import read_from_file
from main import get_top_n_words
from main import remove_stop_words
from main import tokenize

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file((os.path.join(current_dir, 'stop_words.txt')))
    stop_words = stop_words.split('\n')

    #  here goes your logic: calling methods from concordance.py
    tokens = tokenize(data)[:10]
    print('First ten tokens: ', tokens)

    new_tokens = remove_stop_words(tokens, stop_words)
    print('Stop words are now removed: ', new_tokens)

    frequencies = calculate_frequencies(new_tokens)
    print('The frequencies of those tokens are: ', frequencies)

    top_n = get_top_n_words(frequencies, 3)
    print('Первые n по популярности слов :', top_n)

    concordance = get_concordance(new_tokens, 'tired', 1, 3)
    print('Concordance for a searched token "sick" looks like: ', concordance)

    adjacent_words = get_adjacent_words(tokens, 'sick', 1, 3)
    print('Adjacent words for token "sick" are: ', adjacent_words)

    RESULT = concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['feels', 'sick', 'tired', 'worn', 'sleepy']], 'Concordance not working'

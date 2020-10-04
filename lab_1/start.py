"""
Concordance implementation starter
"""

import os

from main import read_from_file
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import get_concordance
from main import get_adjacent_words

if __name__ == '__main__':
    # use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    stop_words = stop_words.split()

    string = tokenize(data)[:10]
    print("First ten tokens look like this: ", string)

    string_new = remove_stop_words(string, stop_words)
    print("The tokens are now clear of stop words: ", string_new)

    dictionary = calculate_frequencies(string_new)
    print("Frequencies of words are now counted: ", dictionary)

    top_n = get_top_n_words(dictionary, 3)
    print("Here are top n popular words: ", top_n)

    concordance = get_concordance(string_new, 'sick', 1, 2)
    print("Concordance for token 'sick' looks like this: ", concordance)

    adjacent_words = get_adjacent_words(string, 'sick', 1, 2)
    print("Here are the adjacent words: ", adjacent_words)

    #  here goes your logic: calling methods from concordance.py

    RESULT = concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['feels', 'sick', 'worn', 'tired']], 'Concordance not working'

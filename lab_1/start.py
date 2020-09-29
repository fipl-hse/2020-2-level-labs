"""
Concordance implementation starter
"""
import os
from main import read_from_file
from main import tokenize
from main import remove_stop_words
#from main import calculate_frequencies
#from main import get_top_n_words
#from main import get_concordance
#from main import get_adjacent_words
#from main import write_to_file
from main import sort_concordance


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    stop_words = stop_words.split ('\n')

    #  here goes your logic: calling methods from concordance.py

    tokens = tokenize(data)
    tokens = remove_stop_words(tokens, stop_words)
    #freq_dict = calculate_frequencies(tokens)
    #top_words = get_top_n_words(freq_dict, 2)
    #concordance = get_concordance(tokens, 'happy', 2, 3)
    #adjacent_words = get_adjacent_words(tokens, 'happy', 1, 2)
    #write_to_file('report.txt', concordance)
    sorted_concordance = sort_concordance(tokens, 'tex', 4, 14, True)

    RESULT = sorted_concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['a', 'leadership', 'challenge', 'compact',
                       'tex', 'xml', 'structuring', 'promises',
                       'make', 'widely', 'usable', 'instant', 'display',
                       'applications', 'web', 'browsers', 'facilitates',
                       'interpretation', 'meaning']], 'Concordance not working'

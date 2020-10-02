"""
Concordance implementation starter
"""

from main import read_from_file
import os

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []

    #  here goes your logic: calling methods from concordance.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    
    tokens = main.tokenize(data)
    print('tokenize', tokens[:10])

    tokens = main.remove_stop_words(tokens, stop_words)
    print('remove_stop_words', tokens[:10])

    frequencies = main.calculate_frequencies(tokens[:5000])
    print('calculate_frequencies', frequencies[tokens[0]])

    concordance = main.get_concordance(tokens, 'name', 3, 0)
    print('get_concordance', concordance[:5])

    adjacent = main.get_adjacent_words(tokens, 'name', 2, 0)
    print('get_adjacent_words', adjacent[:5])

    sorted_concordance = main.sort_concordance(tokens, 'name', 5, 2, True)
    print('sort_concordance', sorted_concordance[:5])

    RESULT = sorted_concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'

"""
Concordance implementation starter
"""

from main import read_from_file
import os
import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = ['the', 'is']

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data[:40])

    token_stw = main.remove_stop_words(tokens, stop_words)

    freq = main.calculate_frequencies(tokens[:20])

    top_words = main.get_top_n_words(freq, 2)

    concordance = main.get_concordance(token_stw[:20], 'team', 1, 1)

    adj_words = main.get_adjacent_words(tokens, 'team', 2, 2)

    file = main.read_from_file('report.txt', concordance)




    RESULT = tokens
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ['years', 'of', 'time', 'team', 'presented', 'a', 'roundup', 'of', 'what', 'has'],'Concordance not working'

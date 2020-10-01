"""
Concordance implementation starter
"""

import os
import main
from main import read_from_file


if __name__ == '__main__':
    # use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = []
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))
    tokens = main.tokenize(data)
    print("tokens, please:", tokens[:50])

    tokens_stop_words = main.remove_stop_words(tokens, stop_words)
    print("tokens without stop words:", tokens_stop_words[:50])

    frequencies = main.calculate_frequencies(tokens_stop_words[:10])
    print("frequency:", frequencies[tokens_stop_words[0]])

    top_words = main.get_top_n_words(frequencies, 4)
    print("top 4 words:", top_words)

    concordance = main.get_concordance(tokens, 'islands', 2, 3)
    print("this is concordance:", concordance[:5])

    adjacent_words = main.get_adjacent_words(tokens, 'islands', 2, 3)
    print("adjacent words for 'book':", adjacent_words[:4])

    main.write_to_file('report.txt', top_words)


    # here goes your logic: calling methods from concordance.py

    RESULT = None
    RESULT = top_words
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'
    #assert RESULT == [(), ()], 'Concordance not working'
    assert RESULT == ['years', 'team', 'presented', 'roundup'], 'Concordance not working'
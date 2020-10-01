"""
Concordance implementation starter
"""

import os
import main


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))

    #  here goes your logic: calling methods from concordance.py

    tokens = main.tokenize(data)
    print("tokens:", tokens[:20])

    tokens_stop_words = main.remove_stop_words(tokens, stop_words)
    print("tokens without stop words:", tokens_stop_words[:20])

    frequencies = main.calculate_frequencies(tokens_stop_words[:5000])
    print("frequency:", frequencies[tokens_stop_words[0]])

    top_words = main.get_top_n_words(frequencies, 4)
    print("top words:", top_words)

    concordance = main.get_concordance(tokens, 'century', 2, 3)
    print(" concordance:", concordance[:5])

    adjacent_words = main.get_adjacent_words(tokens, 'article', 2, 3)
    print("adjacent words :", adjacent_words[:4])

    main.write_to_file('report.txt', sorted_concordance)
    print("File was written successfully")

    # here goes your logic: calling methods from concordance.py

    RESULT = None
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [(), ()], 'Concordance not working'
    assert RESULT, 'Concordance not working'



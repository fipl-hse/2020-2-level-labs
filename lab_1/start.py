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
    print(f"first 7 tokens: {tokens[:7]}")

    tokens = main.remove_stop_words(tokens, stop_words)
    print(f"first 7 tokens without stop words: {tokens[:7]}")

    frequencies = main.calculate_frequencies(tokens)
    print(f"frequency for the first word: {tokens[0]}")

    top_5 = main.get_top_n_words(frequencies, 3)
    print(f"top 5 words: {top_5}")

    mountain_concordance = main.get_concordance(tokens, 'mountain', 2, 3)
    print(f"concordance for 'mountain': {mountain_concordance}")

    mountain_adjacent_words = main.get_adjacent_words(tokens, 'mountain', 1, 1)
    print(f"adjacent words for 'mountain': {mountain_adjacent_words}")

    mountain_sorted_concordance = main.sort_concordance(tokens, 'mountain', 1, 2, True)
    print(f"sorted concordance for 'mountain': {mountain_sorted_concordance}")

    main.write_to_file('report.txt', mountain_sorted_concordance)
    RESULT = mountain_sorted_concordance[:1]

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['shadow', 'mountain', 'p', 'release']], 'Concordance not working'

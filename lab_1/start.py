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
    stop_words = stop_words.split()

    #  here goes your logic: calling methods from concordance.py
    list_of_tokens = main.tokenize(data)
    print('tokenize:', list_of_tokens[:20])

    new_tokens = main.remove_stop_words(list_of_tokens, stop_words)
    print('remove_stop_words:', new_tokens[:20])

    freq_dict = main.calculate_frequencies(new_tokens[:10000])
    print('calculate_frequencies, first elem:', freq_dict[new_tokens[0]])

    top_words = main.get_top_n_words(freq_dict, 5)
    print('top 5 words:', top_words)

    concordance = main.get_concordance(new_tokens, 'people', 1, 2)
    print('get_concordance for "people"', concordance[:3])

    adjacent_words = main.get_adjacent_words(new_tokens, 'people', 1, 2)
    print('get_adjacent_words for "people"', adjacent_words[:3])

    sorted_conc = main.sort_concordance(new_tokens, 'people', 1, 2, True)
    print('sort_concordance for "people"', sorted_conc[:3])

    main.write_to_file('report.txt', sorted_conc)

    RESULT = sorted_conc[:3]
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['a', 'people', 'bent', 'conquest'],
                      ['a', 'people', 'mover', 'station'],
                      ['address', 'people', 'internet', 'politeness']], 'Concordance not working'

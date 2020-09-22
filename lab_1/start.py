"""
Concordance implementation starter
"""

import main


if __name__ == '__main__':
    #  use data.txt file to test your program
    data = main.read_from_file('data.txt')
    stop_words = main.read_from_file('stop_words.txt')

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('tokenize', tokens[:5])
    tokens = main.remove_stop_words(tokens, stop_words)
    print('remove_stop_words', tokens[:5])
    frequencies = main.calculate_frequencies(tokens)
    print('calculate_frequencies', frequencies[tokens[0]])
    concordance = main.get_concordance(tokens, 'dog', 2, 0)
    print('get_concordance', concordance[:5])
    adjacent = main.get_adjacent_words(tokens, 'dog', 2, 0)
    print('get_adjacent_words', adjacent[:5])
    sorted_concordance = main.sort_concordance(tokens, 'dog', 2, 0, True)
    print('sort_concordance', sorted_concordance[:5])
    main.write_to_file('', sorted_concordance)
    RESULT = (isinstance(sorted_concordance) is list) and (all(isinstance(s) is list for s in sorted_concordance))
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'

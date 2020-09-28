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
    print("tokens:", tokens[:10])

    tokens = main.remove_stop_words(tokens, stop_words)
    print("tokens without stop words:", tokens[:10])

    frequencies = main.calculate_frequencies(tokens)
    print("frequency for the first word:", frequencies[tokens[0]])

    top_5_words = main.get_top_n_words(frequencies, 5)
    print("top 5 words:", top_5_words)

    concordance = main.get_concordance(tokens, "book", 2, 3)
    print("concordance for 'book':", concordance[:5])

    adjacent_words = main.get_adjacent_words(tokens, "book", 2, 3)
    print("adjacent words for 'book':", adjacent_words[:5])

    sorted_concordance = main.sort_concordance(tokens, "book", 2, 3, False)
    print("sorted concordance for 'book':", sorted_concordance[:3])

    main.write_to_file('report.txt', sorted_concordance)

    RESULT = sorted_concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['corresponds', 'assigning', 'book', 'a', 'unique', 'identifier'],
                      ['book', 'refer', 'book', 'a', 'relative', 'victim'],
                      ['aerospace', 'source', 'book', 'a', 'village',
                       'voice']], 'Concordance not working'  # result == то, что ожидаем от функции?

"""
Concordance implementation starter
"""

import os
import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = (main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))).split('\n')

    #  here goes your logic: calling methods from concordance.py
    print('    ...tokenizing the text...')
    print('    ...removing stop words...')
    tokens = main.remove_stop_words(main.tokenize(data), stop_words)
    frequencies = main.calculate_frequencies(tokens)
    print('    ...calculating frequencies...')
    top_n_words_list = main.get_top_n_words(frequencies, 10)
    TOP_N_WORDS = ''
    for word in top_n_words_list:
        TOP_N_WORDS += word
        if top_n_words_list.index(word) != (len(top_n_words_list) - 1):
            TOP_N_WORDS += ', '
    print('\n> Top 10 most mentioned words in the text:')
    print(TOP_N_WORDS)
    print("\n    ...getting a concordance of the word 'season'...")
    concordance = main.get_concordance(tokens, 'season', 2, 3)
    EXAMPLE = ''
    for word in concordance[0]:
        EXAMPLE += word
        if concordance[0].index(word) != (len(concordance[0]) - 1):
            EXAMPLE += ', '
    print("\n> The first context of the word 'season' mentioned in the text:")
    print(EXAMPLE)
    adj_words = main.get_adjacent_words(tokens, 'season', 2, 3)
    adj_words_example = adj_words[0]
    adj_word_right = adj_words_example.pop()
    adj_word_left = adj_words_example.pop()
    print("""> Adjacent words from this context: \n'" + adj_word_left + "' as 2nd on the left, \n'" +
    adj_word_right + "' as 3rd on the right""")
    print('\n\n    ...sorting the concordance...')
    sorted_concordance = main.sort_concordance(tokens, 'season', 2, 3, True)
    SORTED_EXAMPLE = ''
    if len(sorted_concordance):
        for word in sorted_concordance[0]:
            SORTED_EXAMPLE += word
            if sorted_concordance[0].index(word) != (len(sorted_concordance[0]) - 1):
                SORTED_EXAMPLE += ', '
    print("\n> The first context of the word 'season' \n(alphabetic order by left context):")
    print(SORTED_EXAMPLE)
    print("\n\n    ...writing the concordance to file 'report.txt'...")
    main.write_to_file(os.path.join(current_dir, 'report.txt'), concordance)

    RESULT = sorted_concordance[:2]
    print(sorted_concordance[:2])
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['disappointing', 'record', 'season', 'saints', 'ended', 'season'],
                      ['saints', 'ended', 'season', 'philosophy', 'mathematics', 'selected']], 'Concordance not working'

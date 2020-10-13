"""
Concordance implementation starter
"""

import os
import main
<<<<<<< HEAD
=======

>>>>>>> upstream/master

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
<<<<<<< HEAD
    stop_words = ['of', 'a']
=======
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt')).split('\n')
>>>>>>> upstream/master

    #  here goes your logic: calling methods from concordance.py
    tokenized_data = main.tokenize(data)
    clean_data = main.remove_stop_words(tokenized_data, stop_words)

    top_n = main.get_top_n_words(main.calculate_frequencies(clean_data), 13)
    key_word = top_n[-1]
    print(f'13th popular word: {key_word}. Let`s use if for further functions')

    closest_words = main.get_adjacent_words(clean_data, key_word, 3, 2)
    if len(closest_words) > 0:
        print(f"\nThird words from the left and second words from the right for "
              f"the word '{key_word}' (first 5 cases) are")
        for adjacent_words in closest_words[:5]:
            print('\t', adjacent_words)

    concordances = main.get_concordance(clean_data, key_word, 2, 2)
    if len(concordances) > 0:
        print(f"\nThe first three concordances (with 2 word on the left and 2 on the right)"
              f"for the word '{key_word}' are")
        for context in concordances[:3]:
            print('\t', context)

    sorted_concordance_left = main.sort_concordance(clean_data, key_word, 2, 2, True)
    if len(sorted_concordance_left) > 0:
        print('\nConcordance sorted by the first left word (first 5 cases):')
        for concordance in sorted_concordance_left[:5]:
            print('\t', concordance)

    sorted_concordance_right = main.sort_concordance(clean_data, key_word, 2, 2, False)
    if len(sorted_concordance_right) > 0:
        print('\nConcordance sorted by the first right word (first 5 cases):')
        for concordance in sorted_concordance_right[:5]:
            print('\t', concordance)

<<<<<<< HEAD
    tokens = main.tokenize(data)
    print(f'TOKENIZE >> {tokens[:10]}')

    tokens = main.remove_stop_words(tokens, stop_words)
    print(f'REMOVE STOPWORDS >> {tokens[:10]}')

    freqs = main.calculate_frequencies(tokens[:5000])
    print(f'CALCULATE FREQUENCIES >> {freqs[tokens[2]]} TIMES')

    concordance = main.get_concordance(tokens, '195', 2, 3)
    print(f'GET CONCORDANCE >> {concordance[:2]}')

    adjacent_words = main.get_adjacent_words(tokens, '195', 2, 3)
    print(f'GET ADJACENT WORDS >> {adjacent_words[:2]}')

    sorted_concordance = main.sort_concordance(tokens, '195', 2, 3, False)
    print(f'SORT CONCORDANCE >> {sorted_concordance[:2]}')

    main.write_to_file('report.txt', sorted_concordance)
    print('WRITE TO FILE >> SUCCESSFUL')

    RESULT = sorted_concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['art', 'pp', '195', '216', 'stained', 'glass'],
                      ['existing', 'ones', '195', 'after', 'he', 'became']], 'Concordance not working'
=======
    RESULT = sorted_concordance_left
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'
>>>>>>> upstream/master

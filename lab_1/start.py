<<<<<<< HEAD
"""
Concordance implementation starter
"""

import os
from lab_1 import main

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))    stop_words = stop_words.split('\n')

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('Tokens:', tokens[:4])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST

    tokens = main.remove_stop_words(tokens, stop_words)
    print('Tokens without stop words:', tokens[:4])

    tokens_frequencies = main.calculate_frequencies(tokens[:5000])
    print('The frequency dictionary of tokens is:', tokens[:10])

    top_n_words = main.get_top_n_words(tokens_frequencies, 20)
    print('Top 20 words:', top_n_words)

    concordance = main.get_concordance(tokens, 'team', 3, 0)
    print("The concordance for word 'task':", concordance[:4])

    adjacent = main.get_adjacent_words(tokens, 'team', 3, 0)
    print("The adjacent for word 'task': ", adjacent[:4])

    main.write_to_file('tokens.txt', top_n_words)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    RESULT = tokens
    assert RESULT == [['years', 'of', 'time', 'team'],
                      ['presented', 'a', 'round', 'up'],
                      ['of', 'what', 'has', 'happened' 'in']], 'Concordance not working'
=======
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

    RESULT = sorted_concordance_left
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Concordance not working'
>>>>>>> 40e50ab46a3e6c28e73f24b3d4f386a76c96a70c

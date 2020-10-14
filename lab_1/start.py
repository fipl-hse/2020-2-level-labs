<<<<<<< HEAD
"""
Concordance implementation starter
"""

<<<<<<< HEAD
from main import read_from_file
from main import tokenize
from main import remove_stop_words
from main import calculate_frequencies
from main import get_top_n_words
from main import get_concordance
=======
>>>>>>> upstream/master
import os
import main


if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
<<<<<<< HEAD
    text = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file((os.path.join(current_dir, 'stop_words.txt')))
    stop_words = stop_words.split('\n')

    #  here goes your logic: calling methods from concordance.py
    tokens = tokenize(text)[:101]
    print('The first 100 tokens are: {}'. format(tokens))

    tokens = remove_stop_words(tokens, stop_words)
    print('Stop words have been removed: {}'.format(tokens))

    freq_dict = calculate_frequencies(tokens)
    print('The frequency dictionary of tokens is: {}'. format(freq_dict))

    top_words = get_top_n_words(freq_dict, 3)
    print('There are three the most popular words: {}'. format(top_words))

    concordance = get_concordance(tokens, 'division', 2, 3)
    print('The concordance for the token "division" is: {}'. format(concordance))

    RESULT = concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == [['recommended', 'a', 'division', 'main', 'services', 'relocation']], 'Concordance not working'
=======
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
>>>>>>> upstream/master
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
>>>>>>> 269900b2ff045e72077421b44012606b226742b0

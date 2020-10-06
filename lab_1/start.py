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
    list_stop_words = stop_words.split()

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print(f"First 15 tokens: {tokens[:15]}")

    cleaned_tokens = main.remove_stop_words(tokens, list_stop_words)
    print(f"First 15 tokens without stop words: {cleaned_tokens[:15]}")

    tokens_frequencies = main.calculate_frequencies(cleaned_tokens[:3000])
    third_token = cleaned_tokens[2]
    print(f"Frequency of the third word: {tokens_frequencies[third_token]}")

    top_5_words = main.get_top_n_words(tokens_frequencies, 5)
    print(f"Top 5 words: {top_5_words}")

    family_concordance = main.get_concordance(cleaned_tokens, "family", 2, 3)
    print(f"Part of concordance for 'family': {family_concordance[:4]}")

    family_adjacent_words = main.get_adjacent_words(cleaned_tokens, 'family', 2, 2)
    print(f"Part of adjacent words (left = 2, right = 3) for 'family': {family_adjacent_words[:4]}")

    family_sorted_concordance = main.sort_concordance(cleaned_tokens, 'family', 1, 2, False)
    print(f"Part of sorted concordance for 'family': {family_sorted_concordance[:4]}")

    main.write_to_file('report.txt', family_sorted_concordance)

    RESULT = family_sorted_concordance
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert [['woman', 'family', 'assist', 'a'], ['pythoninae', 'family', 'boidae', 'boas'],
            ['recommendation', 'family', 'cautioned', 'heisenberg'],
            ['reverted', 'family', 'childless', 'children']], 'Concordance not working'


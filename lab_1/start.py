"""
Concordance implementation starter
"""

import os
from lab_1 import main
from lab_1.main import read_from_file

if __name__ == '__main__':
    #  use data.txt file to test your program
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = read_from_file(os.path.join(current_dir, 'stop_words.txt')).split()

    #  here goes your logic: calling methods from concordance.py
    tokens = main.tokenize(data)
    print('Tokens:', tokens[:20])

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST

    tokens = main.remove_stop_words(tokens, stop_words)
    print('Tokens without stop words:', [tokens[:100]])

    tokens_frequencies = main.calculate_frequencies(tokens)
    print('The frequency dictionary of tokens is:', tokens[:10])

    top_n_words = main.get_top_n_words(tokens_frequencies, 20)
    print('Top 20 words:', top_n_words)

    concordance = main.get_concordance(tokens, 'end', 2, 3)
    print("The concordance for word 'task':", concordance[:6])

    adjacent = main.get_adjacent_words(tokens, 'end', 2, 3)
    print("The adjacent for word 'task': ", adjacent)

    main.write_to_file('tokens.txt', top_n_words)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    RESULT = top_n_words
    assert RESULT == [['an', 'unusually', 'early', 'end', 'to', 'his', 'career', 'in', 'the'],
                      ['and', 'sometimes', 'they', 'end', 'them', 'literally', 'with', 'carved', 'wisps'],
                      ['and', 'towards', 'the', 'end', 'of', 'that', 'century', 'a', 'number'],
                      ['army', 'at', 'the', 'end', 'of', 'season', 'the', 'vfl'],
                      ['at', 'the', 'northwestern', 'end', 'of', 'the', 'island', 'although', 'the'],
                      ['at', 'the', 'other', 'end', 'the', 'two', 'men', 'were', 'arrested'],
                      ['atoms', 'at', 'the', 'end', 'of', 'guerrilla', 'forces', 'numbered', 'no'],
                      ['babylonians', 'to', 'the', 'end', 'of', 'the', 'reading', 'his', 'friends'],
                      ['beach', 'at', 'the', 'end', 'of', 'la', 'dolce', 'vita', 'has'],
                      ['birthday', 'to', 'the', 'end', 'of', 'the', 'year', 'its', 'one']], 'Concordance not working'

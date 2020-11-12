"""
Concordance implementation starter
"""


import os
import main


if __name__ == '__main__':
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data = main.read_from_file(os.path.join(current_dir, 'data.txt'))
    stop_words = main.read_from_file(os.path.join(current_dir, 'stop_words.txt'))

    tokens = main.tokenize(data)
    print(f'Raw text: {data[:5]}')
    print(f'Tokenized text: {tokens[:5]}')

    tokens = main.remove_stop_words(tokens, stop_words)
    print(f'Text without stop-words: {tokens[:5]}')

    frequencies = main.calculate_frequencies(tokens[:5000])
    print(f'Frequencies: {frequencies[tokens[0]]}')

    word = 'dog'
    concordance = main.get_concordance(tokens, word, 2, 0)
    print(f'The concordance for {word}: {concordance[:5]}')

    adjacent = main.get_adjacent_words(tokens, 'dog', 2, 0)
    print(f'Adjacent words: {adjacent[:5]}')

    sorted_concordance = main.sort_concordance(tokens, 'dog', 2, 0, True)
    print(f'Sorted concordance: {sorted_concordance[:5]}')

    main.write_to_file('', sorted_concordance)

    RESULT = sorted_concordance
    assert RESULT, 'Concordance not working'

"""
Language detector implementation starter
"""

import main

if __name__ == '__main__':
    text = 'Horse is beautiful. Dog is beautiful.'
    tokens = main.tokenize_by_sentence(text)
    print(tokens)

    storage = main.LetterStorage()
    storage.update(tokens)
    print(storage.storage)

    encoded_corpus = main.encode_corpus(storage, tokens)
    print(encoded_corpus)

    three_gram = main.NGramTrie(3)
    filles = three_gram.fill_n_grams(encoded_corpus)
    frequencies = three_gram.calculate_n_grams_frequencies()
    top = three_gram.top_n_grams(5)
    print('Frequencies: ', frequencies)
    print('Top 5: ', top)

    RESULT = top
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, ((1, 7, 5), (7, 5, 1), (1, 8, 6), (8, 6, 9), (6, 9, 10))
    'Not working'

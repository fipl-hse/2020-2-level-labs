"""
Language detector implementation starter
"""

import main

if __name__ == '__main__':

    text = 'She is happy. He is happy.'
    tokens = main.tokenize_by_sentence(text)
    print(tokens)

    storage = main.LetterStorage()
    storage.update(tokens)
    print(storage.storage)

    encoded_corpus = main.encode_corpus(storage, tokens)
    print(encoded_corpus)

    bi_gram = main.NGramTrie(2)
    filles = bi_gram.fill_n_grams(encoded_corpus)
    frequencies = bi_gram.calculate_n_grams_frequencies()
    top = bi_gram.top_n_grams(5)
    print('Frequencies: ', frequencies)
    print('Top 5: ', top)

    RESULT = top
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ((1, 1),), 'Not working'

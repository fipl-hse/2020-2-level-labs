"""
Language detector implementation starter
"""

import main

if __name__ == '__main__':
    TEXT = 'Horse is beautiful. Dog is beautiful.'
    TOKENS = main.tokenize_by_sentence(TEXT)
    print(TOKENStokens)

    storage = main.LetterStorage()
    storage.update(TOKENS)
    print(storage.storage)

    encoded_corpus = main.encode_corpus(storage, TOKENS)
    print(encoded_corpus)

    three_gram = main.NGramTrie(3)
    FILLED = three_gram.fill_n_grams(encoded_corpus)
    FREQS = three_gram.calculate_n_grams_frequencies()
    TOP = three_gram.top_n_grams(5)
    print('Frequencies: ', FREQS)
    print('Top 5: ', TOP)

    RESULT = TOP
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, ((1, 7, 5), (7, 5, 1), (1, 8, 6), (8, 6, 9), (6, 9, 10))
    'Not working'

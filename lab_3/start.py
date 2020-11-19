"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    SENTENCE = 'I love you to the moon and back'
    tokenized_sentence = lab_3.main.tokenize_by_sentence(SENTENCE)
    print(f'TOKENS: {tokenized_sentence}')

    storage = lab_3.main.LetterStorage()
    storage.update(tokenized_sentence)
    print(f'STORAGE: {storage.storage}')

    encoded_corpus = lab_3.main.encode_corpus(storage, tokenized_sentence)
    print(f'ENCODED_CORPUS: {encoded_corpus}')

    n_gram = lab_3.main.NGramTrie(2)
    FILL_N_GRAM = n_gram.fill_n_grams(encoded_corpus)
    FREQUENCIES = n_gram.calculate_n_grams_frequencies()
    top = n_gram.top_n_grams(5)
    print(f'TOP_5: {top}')

    RESULT = top
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ((4, 1), (1, 8), (8, 4), (12, 1), (4, 9)), 'Not working'

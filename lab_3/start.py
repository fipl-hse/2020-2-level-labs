"""
Language detector implementation starter
"""

import lab_3.main
import main

if __name__ == '__main__':

    # here goes your function calls
    text = 'To Sherlock Holmes she is always the woman. I have seldom heard him mention her under any other name.'
    tokens = main.tokenize_by_sentence(text)
    print(tokens)
    storage = main.LetterStorage()
    storage.update(tokens)
    print(storage.storage)

    encoded_corpus = main.encode_corpus(storage, tokens)
    print(encoded_corpus)

    bi_gram = main.NGramTrie(2)
    fille = bi_gram.fill_n_grams(encoded_corpus)
    frequencies = bi_gram.calculate_n_grams_frequencies()
    top = bi_gram.top_n_grams(5)
    print('Frequencies: ', frequencies)
    print('Top 5: ', top)

    RESULT = top
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ((1, 1),), 'Not working'

"""
Language detector implementation starter
"""

import main

if __name__ == '__main__':
    text = 'It aspires to being a modernized fairy tale, in which the wonderment and joy are retained. The heartaches and nightmares are left out.'
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

    # here goes your function calls

    RESULT = top
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Not working'

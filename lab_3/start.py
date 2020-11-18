"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls

    text = "The artist is the creator of beautiful things. " \
           "To reveal art and conceal the artist is art's aim. " \
           "The critic is he who can translate into another manner or " \
           "a new material his impression of beautiful things."

    tokens = lab_3.main.tokenize_by_sentence(text)
    print('Tokens: ', tokens)

    storage = lab_3.main.LetterStorage()
    storage.update(tokens)
    print('Id for letters', storage.storage)

    encoded_corpus = lab_3.main.encode_corpus(storage, tokens)

    n_gram_trie = lab_3.main.NGramTrie(2)
    n_gram_trie.fill_n_grams(encoded_corpus)
    n_gram_trie.calculate_n_grams_frequencies()
    print('Top 5 bi-grams in the text: ', n_gram_trie.top_n_grams(5))

    RESULT = n_gram_trie.top_n_grams(5)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ((0, 1), (1, 2), (4, 5), (3, 0), (6, 7)), 'Something went wrong'
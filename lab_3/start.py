"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls
    text = 'Hi everyone! Nice to meet you! But you`re not... I`m sorry to distract.'
    corpus = lab_3.main.tokenize_by_sentence(text)
    print('This is the corpus of tuples: ', corpus)

    storage = lab_3.main.LetterStorage()
    storage.update(corpus)
    print('This is the code: ', storage.storage)

    text_ind = lab_3.main.encode_corpus(storage, corpus)
    print('This is the encoded corpus: ', text_ind)

    bi_gram_trie = lab_3.main.NGramTrie(2)
    bi_gram_trie.fill_n_grams(text_ind)
    bi_gram_trie.calculate_n_grams_frequencies()
    print('This is the top 2 bi-grams in the text: ', bi_gram_trie.top_n_grams(2))

    RESULT = bi_gram_trie.top_n_grams(2)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ((0, 1), (1, 2))

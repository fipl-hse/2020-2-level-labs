"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls
    text = 'Hi everyone! Nice to meet you! But you`re not... I`m sorry to distract.'
    corpus_of_tuples = lab_3.main.tokenize_by_sentence(text)
    print('This is the corpus of tuples: ', corpus_of_tuples)

    storage = lab_3.main.LetterStorage()
    storage.update(corpus_of_tuples)
    print('Coding with: ', storage.storage)

    encoded_text = lab_3.main.encode_corpus(storage, corpus_of_tuples)
    print('This is the encoded corpus: ', encoded_text)

    bi_gram_trie = lab_3.main.NGramTrie(2)
    bi_gram_trie.fill_n_grams(encoded_text)
    bi_gram_trie.calculate_n_grams_frequencies()
    print('This is the top 4 bi-grams in the text: ', bi_gram_trie.top_n_grams(4))

    RESULT = bi_gram_trie.top_n_grams(4)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, ''

"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls
    text = 'Never stop trying. Believe in you power. Do not give up. Your day will come. Trust me.'

    tuple_with_tokens = lab_3.main.tokenize_by_sentence(text)
    print('Tokens: ', tuple_with_tokens)

    storage = lab_3.main.LetterStorage()
    storage.update(tuple_with_tokens)
    print('Coding with: ', storage.storage)

    encoded_corpus = lab_3.main.encode_corpus(storage, tuple_with_tokens)

    bi_gram_trie = lab_3.main.NGramTrie(2)
    bi_gram_trie.fill_n_grams(encoded_corpus)
    bi_gram_trie.calculate_n_grams_frequencies()
    print('Top 3 bi-grams in the text: ', bi_gram_trie.top_n_grams(3))

    RESULT = bi_gram_trie.top_n_grams(3)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ((4, 3), (5, 1), (7, 5)), 'Something went wrong :('

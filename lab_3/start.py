"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls
    text = "She say, 'Do you love me?' I tell her, 'Only partly'.I only love my bed and my momma, I'm sorry"
    tuple_with_tokens = lab_3.main.tokenize_by_sentence(text)
    storage = lab_3.main.LetterStorage()
    storage.update(tuple_with_tokens)
    encoded_corpus = lab_3.main.encode_corpus(storage, tuple_with_tokens)
    n_gram = lab_3.main.NGramTrie(2)
    n_gram.fill_n_grams(encoded_corpus)
    n_gram.calculate_n_grams_frequencies()
    print('Top 5 bi-grams in the text: ', n_gram.top_n_grams(5))

    RESULT = n_gram.top_n_grams(5)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, ''

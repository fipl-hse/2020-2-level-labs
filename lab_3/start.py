"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls
    text = 'The, first sentence - nice. The second sentence: bad!'
    sent=lab_3.main.tokenize_by_sentence(text)
    print(sent)

    storage=lab_3.main.LetterStorage()
    storage.update(sent)

    encoded_corpus=lab_3.main.encode_corpus(storage,sent)
    print(encoded_corpus)

    bi_gram=lab_3.main.NGramTrie(2)
    filled_bi_gram=bi_gram.fill_n_grams(encoded_corpus)
    freq=bi_gram.calculate_n_grams_frequencies()
    print(freq)

    top_3=bi_gram.top_n_grams(3)
    print(top_3)

    expected=((3, 0), (3, 8), (0, 7))
    actual=top_3
    RESULT = actual
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT==expected, 'Result differ'

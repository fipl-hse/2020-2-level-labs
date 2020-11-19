"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls

    text = 'To Sherlock Holmes she is always the woman. I have seldom heard him mention her under any other name.'
    tokenized_text = lab_3.main.tokenize_by_sentence(text)
    print(tokenized_text)

    letter_storage = lab_3.main.LetterStorage()
    letter_storage.update(tokenized_text)
    encoded_text = lab_3.main.encode_corpus(letter_storage, tokenized_text)
    print(encoded_text)

    bi_gram = lab_3.main.NGramTrie(2)
    filled_bi_grams = bi_gram.fill_n_grams(encoded_text)
    bi_grams_frequencies = bi_gram.calculate_n_grams_frequencies()
    top_bi_grams = bi_gram.top_n_grams(5)
    print('Top 5 bi_grams: ', top_bi_grams)

    RESULT = top_bi_grams
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ((9, 10), (5, 9), (10, 11), (10, 5), (5, 8)), 'Not working'

"""
Language detector implementation starter
"""

import lab_3.main

if __name__ == '__main__':

    # here goes your function calls
    text = "Once Mr Stamp-About went though Dimity Wood in a great rage. " \
           "He stamped as he went and muttered to himself, and he even shook his first in the air."
    text_with_letters = lab_3.main.tokenize_by_sentence(text)
    print('Letters in the text: ', text_with_letters)

    letter_storage = lab_3.main.LetterStorage()
    letter_storage.update(text_with_letters)
    print('Dictionary with letters and their values: ', letter_storage.storage)

    encoded_text = lab_3.main.encode_corpus(letter_storage, text_with_letters)

    bi_gram = lab_3.main.NGramTrie(2)
    bi_gram.fill_n_grams(encoded_text)
    bi_gram.calculate_n_grams_frequencies()
    print('Top 7 bi-grams: ', bi_gram.top_n_grams(7))

    RESULT = bi_gram.top_n_grams(7)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT == ((0, 1), (8, 9), (4, 0), (9, 5), (1, 2), (5, 6), (2, 3)), "Something went wrong"

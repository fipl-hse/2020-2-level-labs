"""
Text generator implementation starter
"""

from lab_4.main import WordStorage
from lab_4.main import tokenize_by_sentence, encode_text

if __name__ == '__main__':
    # here goes your function calls
    first_text = open('lab_3/Frank_Baum.txt', encoding="utf-8")
    second_text = open('lab_3/Thomas_Mann.txt', encoding="utf-8")

    first_text_tokenized = tokenize_by_sentence(first_text.read())
    second_text_tokenized = tokenize_by_sentence(second_text.read())

    word_storage = WordStorage()
    word_storage.update(first_text_tokenized)
    word_storage.update(second_text_tokenized)

    first_text_encoded = encode_text(word_storage, first_text_tokenized)
    second_text_encoded = encode_text(word_storage, second_text_tokenized)

    assert first_text_encoded, "Not working"
    assert second_text_encoded, "Not working"

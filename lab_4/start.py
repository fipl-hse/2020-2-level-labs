"""
Text generator implementation starter
"""

from lab_4.main import WordStorage
from lab_4.main import tokenize_by_sentence, encode_text

if __name__ == '__main__':
    # here goes your function calls
    first_text = open('../lab_3/Frank_Baum.txt', encoding="utf-8")
    first_text_tokenized = tokenize_by_sentence(first_text.read())

    word_storage = WordStorage()
    word_storage.update(first_text_tokenized)

    RESULT = encode_text(word_storage, first_text_tokenized)

    assert RESULT, "Not working"

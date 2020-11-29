"""
Lab 4 implementation starter
"""

from lab_4.main import tokenize_by_sentence, encode_text, WordStorage


if __name__ == '__main__':
    text = 'Mar#y wa$nted, to swim. However, she was afraid of sharks.'
    tokenized_text = tokenize_by_sentence(text)
    word_storage = WordStorage()
    word_storage.update(tokenized_text)
    encoded_text = encode_text(word_storage, tokenized_text)

    RESULT = len(encoded_text) == len(tokenized_text)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Encoding not working'

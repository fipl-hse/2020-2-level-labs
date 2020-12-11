"""
Lab 4 implementation starter
"""

from lab_4.main import WordStorage, NGramTrie, NGramTextGenerator
from lab_4.main import tokenize_by_sentence, encode_text

if __name__ == '__main__':
    text = 'She has a house. He has a house too. Besides he has a car. My friend also he has a car. ' \
           'Seems like everyone has has a car, but me.'

    text_tokenized = tokenize_by_sentence(text)

    word_storage = WordStorage()
    word_storage.update(text_tokenized)

    encoded_text = encode_text(word_storage, text_tokenized)
    print(encoded_text)

    trie = NGramTrie(2, encoded_text)
    context = (word_storage.get_id('has'),)
    generator = NGramTextGenerator(word_storage, trie)

    actual = generator.generate_text(context, 4)

    RESULT = actual
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, "Something went wrong"
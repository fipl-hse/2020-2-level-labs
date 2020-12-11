"""
Text generator implementation starter
"""

from lab_4.main import WordStorage, NGramTrie, NGramTextGenerator
from lab_4.main import tokenize_by_sentence, encode_text

if __name__ == '__main__':
    TEXT = 'I have a cat. His name is Bruno. I have a dog. Her name is Bobic. Her name is Bobic too.'
    text_tokenized = tokenize_by_sentence(TEXT)

    word_storage = WordStorage()
    word_storage.update(text_tokenized)

    encoded = encode_text(word_storage, text_tokenized)

    trie = NGramTrie(2, encoded)
    context = (word_storage.get_id('i'),)
    generator = NGramTextGenerator(word_storage, trie)

    RESULT = generator.generate_text(context, 4)

    print(RESULT)

    assert RESULT, "Not working"
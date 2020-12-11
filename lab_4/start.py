"""
Lab 4
"""

from lab_4.main import WordStorage,  tokenize_by_sentence, encode_text, NGramTextGenerator
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    text = 'I have a cat. His name is Bruno. I have a dog. Her name is Rex. Her name is Rex too.'
    text_tokenized = tokenize_by_sentence(text)

    word_storage = WordStorage()
    word_storage.update(text_tokenized)

    encoded = encode_text(word_storage, text_tokenized)

    trie = NGramTrie(2, encoded)
    context = (word_storage.get_id('i'),)
    generator = NGramTextGenerator(word_storage, trie)

    RESULT = generator.generate_text(context, 4)

    print(RESULT)

    assert RESULT, "Not working"

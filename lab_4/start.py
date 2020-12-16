"""
Lab 4 implementation starter
"""

from lab_4.main import tokenize_by_sentence, WordStorage, encode_text, NGramTextGenerator
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    text = 'I have a dog.\nHis name is Will'
    tokenize_text = tokenize_by_sentence(text)
    print(tokenize_text)

    storage = WordStorage()
    storage.update(tokenize_text)
    print(storage)

    encode = encode_text(storage, tokenize_text)
    print(encode)

    n_gram_trie = NGramTrie(2, encode)
    print(n_gram_trie)
    generator = NGramTextGenerator(storage, n_gram_trie)
    context = (storage.get_id('a'),)
    print(context)

    RESULT = generator.generate_text(context, 3)
    print(RESULT)
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Not working'

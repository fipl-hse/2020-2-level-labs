"""
Lab 4 implementation starter
"""

from lab_4.main import BackOffGenerator, encode_text, WordStorage, decode_text, tokenize_by_sentence
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    with open('lab_3/Frank_Baum.txt', 'r', encoding='utf-8') as file_frank:
        corpus = tokenize_by_sentence(file_frank.read())

    storage = WordStorage()
    storage.update(corpus)
    encoded = encode_text(storage, corpus)

    trie = NGramTrie(3, encoded)
    four = NGramTrie(4, encoded)

    context = (storage.get_id('when'),
               storage.get_id('the'),)

    generator = BackOffGenerator(storage, four, trie)
    generated_text = generator.generate_text(context, 5)
    RESULT = decode_text(storage, generated_text)

    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Encoding not working'

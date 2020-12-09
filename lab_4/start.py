"""
Lab 4 starter
"""
from lab_4.main import BackOffGenerator, encode_text, WordStorage, decode_text
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    corpus = ('i', 'have', 'a', 'cat', '<END>',
              'his', 'name', 'is', 'bruno', '<END>',
              'i', 'have', 'a', 'dog', 'too', '<END>',
              'his', 'name', 'is', 'rex', '<END>',
              'her', 'name', 'is', 'rex', 'too', '<END>')
    storage = WordStorage()
    storage.update(corpus)
    encoded_text = encode_text(storage, corpus)
    trie = NGramTrie(3, encoded_text)
    four = NGramTrie(4, encoded_text)
    context = (storage.get_id('his'),
               storage.get_id('name'),
               storage.get_id('is'),)
    generator = BackOffGenerator(storage, trie, four)

    text = generator.generate_text(context, 3)
    actual = decode_text(storage, text)
    RESULT = ('His name is bruno', 'I have a cat', 'His name is bruno')
    assert RESULT == actual, 'Not work'

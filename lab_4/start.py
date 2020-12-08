"""
Lab 4 starter
"""
from lab_4.main import LikelihoodBasedTextGenerator, encode_text, WordStorage
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
    context = (storage.get_id('i'),
               storage.get_id('have'))
    generator = LikelihoodBasedTextGenerator(storage, trie)

    RESULT = generator.generate_text(context, 3)
    assert RESULT, 'Not work'

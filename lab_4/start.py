from lab_4.main import *
import ngrams.ngram_trie as ngrams

if __name__ == '__main__':
    corpus = ('i', 'have', 'a', 'cat', '<END>',
              'his', 'name', 'is', 'bruno', '<END>',
              'i', 'have', 'a', 'dog', 'too', '<END>',
              'his', 'name', 'is', 'rex', '<END>',
              'her', 'name', 'is', 'rex', 'too', '<END>')
    storage = WordStorage()
    storage.update(corpus)
    encoded = encode_text(storage, corpus)
    trie = ngrams.NGramTrie(2, encoded)
    context = (storage.get_id('i'),)

    generator = NGramTextGenerator(storage, trie)
    actual = generator.generate_text(context, 5)
    actual = decode_text(storage, actual)
    print(actual)

    generator = LikelihoodBasedTextGenerator(storage, trie)
    actual = generator.generate_text(context, 5)
    actual = decode_text(storage, actual)
    print(actual)

    two = ngrams.NGramTrie(2, encoded)
    trie = ngrams.NGramTrie(3, encoded)

    context = (storage.get_id('name'),
               storage.get_id('is'),)

    generator = BackOffGenerator(storage, trie, two)

    actual = generator.generate_text(context, 5)
    actual = decode_text(storage, actual)
    print(actual)

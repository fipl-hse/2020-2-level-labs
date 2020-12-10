from lab_4.main import WordStorage, encode_text
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    corpus = ('i', 'have', 'a', 'cat', '<END>',
              'his', 'name', 'is', 'leon', '<END>',
              'i', 'have', 'a', 'dog', 'too', '<END>',
              'his', 'name', 'is', 'taylor', '<END>',
              'her', 'name', 'is', 'taylor', 'too', '<END>')

    storage = WordStorage()
    storage.update(corpus)

    encoded = encode_text(storage, corpus)

    trie = NGramTrie(3, encoded)

    context = (storage.get_id('i'),
               storage.get_id('have'),)


    RESULT = decode_text(storage, generated_text)

    assert RESULT ==
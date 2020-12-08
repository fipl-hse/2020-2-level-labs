import main
import ngrams

if __name__ == '__main__':
    text = 'I have a cat.\nHis name is Bruno'
    corpus = main.tokenize_by_sentence(text)
    print(corpus)

    storage = main.WordStorage()
    storage.update(corpus)
    print(storage.storage)

    encoded = main.encode_text(storage, corpus)
    print(encoded)

    trie = ngrams.ngram_trie.NGramTrie(2, encoded)

    context = (storage.get_id('name'),
               storage.get_id('is'),)
    print(context)

    generator = main.NGramTextGenerator(storage, trie)

    text = generator.generate_text(context, 2)

    RESULT = text
    assert RESULT == (5, 5), 'Not working'

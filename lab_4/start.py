import unittest
from lab_4.main import tokenize_by_sentence, encode_text, WordStorage, LikelihoodBasedTextGenerator, decode_text
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':

    text = 'I have a cat.\nHis name is Bruno. \nI have a dog too. \nHis name is rex. \nHer name is rex too.'
    corpus = tokenize_by_sentence(text)

    storage = WordStorage()
    storage.update(corpus)

    encoded = encode_text(storage, corpus)

    trie = NGramTrie(3, encoded)

    context = (storage.get_id('name'),
               storage.get_id('is'),)
    end = storage.get_id('<END>')

    generator = LikelihoodBasedTextGenerator(storage, trie)

    to_decode = generator.generate_text(context, 2)

    expected = ('Name is rex', 'Her name is rex')
    RESULT = decode_text(storage, to_decode)
    print(RESULT)

    assert RESULT == expected, 'doesnt work'

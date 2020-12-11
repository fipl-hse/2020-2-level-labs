from lab_4.main import tokenize_by_sentence, WordStorage, encode_text, NGramTextGenerator
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    TEXT = 'I like flowers.\nMy mom likes flowers too.\nHer favourite flower is rose.\nMy favourite flower is rose too.'
    corpus = tokenize_by_sentence(TEXT)

    word_storage = WordStorage()
    word_storage.update(corpus)

    encoded_corpus = encode_text(word_storage, corpus)

    ngrams = NGramTrie(2, encoded_corpus)

    text_generator = NGramTextGenerator(word_storage, ngrams)
    gen_text = text_generator.generate_text((1,), 2)

    end = word_storage.get_id('<END>')
    actual = gen_text.count(end)
    RESULT = 2
    print(actual)
    assert RESULT == actual, 'not working'
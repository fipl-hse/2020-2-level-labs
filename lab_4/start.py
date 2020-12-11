from lab_4.main import tokenize_by_sentence, WordStorage, encode_text, NGramTextGenerator
from lab_4.ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    TEXT = 'I have a friend. \n Her name is Beth.'
    corpus = tokenize_by_sentence(TEXT)

    word_storage = WordStorage()
    word_storage.update(corpus)

    encoded_corpus = encode_text(word_storage, corpus)

    ngrams = NGramTrie(2, encoded_corpus)

    text_generator = NGramTextGenerator(word_storage, ngrams)

    context = (word_storage.get_id('name'),
               word_storage.get_id('is'))

    gen_text = text_generator.generate_text(context, 2)

    RESULT = gen_text
    assert RESULT == (5,5), 'Not working'
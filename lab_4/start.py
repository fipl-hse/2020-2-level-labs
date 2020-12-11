from lab_4.main import tokenize_by_sentence, WordStorage, encode_text, NGramTextGenerator, NGramTrie

if __name__ == '__main__':
    text = 'I have a friend. \n Her name is Beth.'

    corpus = tokenize_by_sentence(text)

    word_storage = WordStorage()
    word_storage.update(corpus)

    encoded_corpus = encode_text(word_storage, corpus)

    ngrams = NGramTrie(2, encoded_corpus)

    generator = NGramTextGenerator(word_storage, ngrams)

    context = (word_storage.get_id('name'),
               word_storage.get_id('is'))

    text = generator.generate_text(context, 2)

    RESULT = text
    assert RESULT, 'Not working'
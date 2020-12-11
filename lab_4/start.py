"""
 Text generator
 """
import main
import ngrams


if __name__ == '__main__':
    text = 'I want to pass exams. I do not want study morphology'
    corpus = main.tokenize_by_sentence(text)
    word_storage = main.WordStorage()
    word_storage.update(corpus)

    encoded_text = main.encode_text(word_storage, corpus)

    n_gram_trie = ngrams.NGramTrie(2, encoded_text)

    n_gram_text_generator = main.NGramTextGenerator(word_storage, n_gram_trie)

    context = (word_storage.get_id('want'), word_storage.get_id('study'))

    text_generated = n_gram_text_generator.generate_text(context, 2)
    RESULT = text_generated

    assert RESULT, ''
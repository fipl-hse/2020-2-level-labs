from lab_4.ngrams.ngram_trie import NGramTrie
from lab_4.main import WordStorage, NGramTextGenerator, LikelihoodBasedTextGenerator, BackOffGenerator, encode_text, \
    decode_text, tokenize_by_sentence, load_model


def realize_n_gram_text_generator(corpus):
    n_gram_storage = WordStorage()
    n_gram_storage.update(corpus)
    n_gram_context = (n_gram_storage.get_id('my'), n_gram_storage.get_id('dear'))
    n_gram_encoded = encode_text(n_gram_storage, corpus)
    n_gram_trie = NGramTrie(3, n_gram_encoded)
    n_gram_generator = NGramTextGenerator(n_gram_storage, n_gram_trie)
    n_gram_text = n_gram_generator.generate_text(n_gram_context, 3)
    return decode_text(n_gram_storage, n_gram_text)


def realize_likelihood_generator(corpus):
    likelihood_storage = WordStorage()
    likelihood_storage.update(corpus)
    context = (likelihood_storage.get_id('i'),
               likelihood_storage.get_id('shall'),)
    model = load_model('likelihood_model.json')
    generator = LikelihoodBasedTextGenerator(model.word_storage, model.n_gram_trie)
    likelihood_text = generator.generate_text(context, 3)

    return decode_text(likelihood_storage, likelihood_text)


def realize_backoff_generator(corpus):
    backoff_storage = WordStorage()
    backoff_storage.update(corpus)
    backoff_encoded = encode_text(backoff_storage, corpus)
    two = NGramTrie(2, backoff_encoded)
    trie = NGramTrie(3, backoff_encoded)
    backoff_context = (backoff_storage.get_id('if'),
                       backoff_storage.get_id('you'),)
    backoff_generator = BackOffGenerator(backoff_storage, trie, two)
    backoff_text = backoff_generator.generate_text(backoff_context, 3)

    return decode_text(backoff_storage, backoff_text)


if __name__ == '__main__':

    with open('corpus.txt', 'r') as f:
        text_str = f.read()

    corpus = tokenize_by_sentence(text_str)

    n_gram_text = realize_n_gram_text_generator(corpus)
    print(n_gram_text)

    likelihood_text = realize_likelihood_generator(corpus)
    print(likelihood_text)

    backoff_text = realize_backoff_generator(corpus)
    print(backoff_text)

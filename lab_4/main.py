"""
Lab 4
"""
import re
import ast
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    tokenized = []
    sentences = re.split('[.!?]', text)

    for sentence in sentences:
        tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()

        if tokens:
            tokenized.extend(tokens + ['<END>'])

    return tuple(tokenized)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or not word:
            raise ValueError

        if word not in self.storage:
            self.storage[word] = len(self.storage) + 1

        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or not word:
            raise ValueError

        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int) or not word_id:
            raise ValueError

        for word, idx in self.storage.items():
            if idx == word_id:
                return word

        raise KeyError

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError

        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError

    return tuple(storage.get_id(word) for word in text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        left_context = [n_gram for n_gram in self._n_gram_trie.n_grams if context == n_gram[:len(context)]]

        if left_context:
            top_n_grams = sorted(left_context, key=self._n_gram_trie.n_gram_frequencies.get, reverse=True)
            return top_n_grams[0][-1]

        full_context = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)

        return full_context[0][0]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        sent = list(context)

        for _ in range(20):
            sent.append(self._generate_next_word(tuple(sent[-(len(context)):])))

            if sent[-1] == self._word_storage.storage['<END>']:
                break

        else:
            sent.append(self._word_storage.storage['<END>'])

        return tuple(sent)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        sentences = []

        for _ in range(number_of_sentences):
            new_sent = self._generate_sentence(context)

            if new_sent[len(context) - 1] == self._word_storage.storage['<END>']:
                new_sent = new_sent[len(context):]

            sentences.extend(new_sent)
            context = tuple(sentences[-len(context):])

        return tuple(sentences)

    def sample_method(self):
        pass


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if (not isinstance(word, int) or
                not isinstance(context, tuple) or
                not (word,) in self._n_gram_trie.uni_grams or
                len(context) + 1 != self._n_gram_trie.size):
            raise ValueError

        context_freq = 0.0

        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if n_gram[:len(context)] == context:
                context_freq += freq

        if context_freq:
            context_freq = self._n_gram_trie.n_gram_frequencies.get(context + (word,), 0) / context_freq

        return context_freq

    def _generate_next_word(self, context: tuple) -> int:

        if (not isinstance(context, tuple) or
                not context or
                len(context) != self._n_gram_trie.size - 1):
            raise ValueError

        max_freq, word = 0, 0

        for value in self._word_storage.storage.values():
            frequency = self._calculate_maximum_likelihood(value, context)

            if frequency > max_freq:
                max_freq, word = frequency, value

        if not max_freq:
            word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]

        return word

    def sample_method(self):
        pass


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)
        self._n_gram_tries = (n_gram_trie,) + args

    def _generate_next_word(self, context: tuple) -> int:
        if (not isinstance(context, tuple) or
                len(context) + 1 != self._n_gram_trie.size or
                context[0] > len(self._word_storage.storage)):
            raise ValueError

        max_size = len(context) + 1
        self._n_gram_tries = [trie for trie in self._n_gram_tries if trie.size <= max_size]

        for trie in self._n_gram_tries:
            self._n_gram_trie = trie

            if n_gram := super()._generate_next_word(context):
                return n_gram
            context = context[:-1]

        return n_gram


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple):
        raise ValueError

    text = ' '.join(storage.get_word(word) for word in encoded_text) + ' '
    text = text.split(' <END> ')
    text = tuple(sent.capitalize() for sent in text)

    return text[:-1]


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    if not isinstance(model, NGramTextGenerator) or not isinstance(path_to_saved_model, str):
        raise ValueError

    with open(path_to_saved_model, 'w', encoding='utf-8') as obj:
        model_attrs = {x[0]: x[1].__dict__ for x in model.__dict__.items()}
        obj.write(str(model_attrs))


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    if not isinstance(path_to_saved_model, str):
        raise ValueError

    with open(path_to_saved_model) as obj:
        attrs = dict(ast.literal_eval(obj.read()))

    storage = type('WordStorage', (), attrs['_word_storage'])
    trie = type('NGramTrie', (), attrs['_n_gram_trie'])

    class Model(NGramTextGenerator):
        def __init__(self, word_storage, n_gram_trie):
            super().__init__(word_storage, n_gram_trie)
            self.__class__.__name__ = 'NGramTextGenerator'

    model = Model(storage(), trie())

    return model

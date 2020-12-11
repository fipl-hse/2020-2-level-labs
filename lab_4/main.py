"""
Lab 4
"""
import re
from lab_4.ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    sentences = re.split(r'[!?.][ \n]', text)
    listed_tokens = []
    for sentence in sentences:
        sentence = sentence.lower()
        tokens = re.sub(r'[^a-z \n]', '', sentence).split()
        if tokens:
            listed_tokens.extend(tokens)
            listed_tokens.append('<END>')

    return tuple(listed_tokens)


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

    encoded_text = []

    for word in text:
        encoded_word = storage.get_id(word)
        encoded_text.append(encoded_word)

    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if (not isinstance(context, tuple) or
                len(context) != self._n_gram_trie.size - 1 or '<END>' in context):
            raise ValueError

        freqs = []

        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if context == n_gram[:-1]:
                freqs.append(freq)

        if not freqs:
            top_words = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
            return top_words[0][0]

        max_freq = sorted(freqs)[-1]

        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if context == n_gram[:-1] and freq == max_freq:
                return n_gram[-1]
        return 0  # for lint

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

        generated_text = []

        for _ in range(number_of_sentences):
            new_sent = self._generate_sentence(context)

            if new_sent[len(context) - 1] == self._word_storage.storage['<END>']:
                new_sent = new_sent[len(context):]

            generated_text.extend(new_sent)
            context = tuple(generated_text[-len(context):])

        return tuple(generated_text)

    def p_method(self):
        pass


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if (not isinstance(word, int) or
                not isinstance(context, tuple) or
                not (word,) in self._n_gram_trie.uni_grams or
                len(context) + 1 != self._n_gram_trie.size):
            raise ValueError

        try:
            listed_context = list(context)
            listed_context.append(word)
            combination = tuple(listed_context)
            combination_freq = self._n_gram_trie.n_gram_frequencies[combination]

        except KeyError:
            return 0.0

        else:
            context_freq = 0
            for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
                if n_gram[:-1] == context:
                    context_freq += freq

            return combination_freq / context_freq

    def _generate_next_word(self, context: tuple) -> int:
        if (not isinstance(context, tuple) or
                not context or
                len(context) != self._n_gram_trie.size - 1):
            raise ValueError

        max_freq = 0
        word = 0

        for value in self._word_storage.storage.values():
            frequency = self._calculate_maximum_likelihood(value, context)

            if frequency > max_freq:
                max_freq = frequency
                word = value

        if not max_freq:
            word = sorted([freqs for freqs in self._n_gram_trie.uni_grams.values()])[-1]

        return word

    def p_method_1(self):
        pass


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)
        self._n_gram_tries = sorted((n_gram_trie,) + args, key=lambda x: x.size, reverse=True)

    def _generate_next_word(self, context: tuple) -> int:
        if (not isinstance(context, tuple) or
                len(context) + 1 != self._n_gram_trie.size or
                context[0] > len(self._word_storage.storage)):
            raise ValueError

        max_size = len(context) + 1
        tries = [trie for trie in self._n_gram_tries if trie.size <= max_size]

        for trie in tries:
            if [i for i in trie.n_grams if context[:(trie.size - 1)] == i[:(trie.size - 1)]]:
                return super()._generate_next_word(context)

        return super()._generate_next_word(context)


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple):
        raise ValueError

    decoded_text = [storage.get_word(word) for word in encoded_text]
    text = []
    sent = []
    for word in decoded_text:
        if word != '<END>':
            sent.append(word)
        else:
            sentence = ' '.join(sent)
            text.append(sentence)
            sent = []

    text = [sent.capitalize() for sent in text]
    return tuple(text)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

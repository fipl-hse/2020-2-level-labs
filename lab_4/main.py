"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    sentences = re.split(r'[.?!]', text)
    tokens_list = []

    for sentence in sentences:
        tokens = re.sub(r'[^a-z \n]', '', sentence.lower()).split()

        if tokens:
            tokens_list += tokens + ['<END>']

    return tuple(tokens_list)


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

        if word not in self.storage:
            raise KeyError

        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int):
            raise ValueError

        if word_id not in self.storage.values():
            raise KeyError

        for key, value in self.storage.items():
            if value == word_id:
                return key

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError

        for word in corpus:
            self._put_word(word)

        return


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError

    encoded_text = [storage.get_id(word) for word in text]

    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        max_freq_word = ''
        word_frequency = 0
        for n_gram, n_gram_freq in self._n_gram_trie.n_gram_frequencies.items():
            if n_gram[:len(context)] == context and n_gram_freq > word_frequency:
                max_freq_word = n_gram[-1]
                word_frequency = n_gram_freq

        if not max_freq_word:
            max_freq_word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]

        return max_freq_word

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        sentence = list(context)

        for _ in range(20):
            sentence.append(self._generate_next_word(tuple(sentence[-(self._n_gram_trie.size - 1):])))

            if sentence[-1] == self._word_storage.get_id('<END>'):
                break

        if self._word_storage.get_id('<END>') not in sentence:
            sentence.append(self._word_storage.get_id('<END>'))

        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        text = list(context)

        for _ in range(number_of_sentences):
            sentence = self._generate_sentence(tuple(text[-(self._n_gram_trie.size - 1):]))
            text.extend(sentence[1:])

        return tuple(text)


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if not isinstance(word, int) or not isinstance(context, tuple) or\
                not (word,) in self._n_gram_trie.uni_grams or len(context)+1 != self._n_gram_trie.size:
            raise ValueError

        freq_context = sum([n_gram_freq for n_gram, n_gram_freq in self._n_gram_trie.n_gram_frequencies.items()
                            if n_gram[:len(context)] == context])

        if freq_context:
            freq_context = self._n_gram_trie.n_gram_frequencies.get(tuple(context + (word,)), 0) / freq_context

        return freq_context

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size or \
                context[0] > len(self._word_storage.storage):
            raise ValueError

        next_word = 0
        word_frequency = 0

        for word in self._word_storage.storage.values():
            frequency = self._calculate_maximum_likelihood(word, context)
            if frequency > word_frequency:
                word_frequency = frequency
                next_word = word

        if not word_frequency:
            next_word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]

        return next_word


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple) or not encoded_text:
        raise ValueError

    decoded_text = []
    decoded_sentence = []
    for encoded_word in encoded_text:
        decoded_word = storage.get_word(encoded_word)
        if decoded_word == '<END>':
            decoded_text.append(' '.join(decoded_sentence))
            decoded_sentence = []
            continue

        if not decoded_sentence:
            decoded_sentence.append(decoded_word.capitalize())
        else:
            decoded_sentence.append(decoded_word)

def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

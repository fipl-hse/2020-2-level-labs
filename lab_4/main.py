"""
Lab 4
"""

import re
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    tokens = []

    if not isinstance(text, str):
        raise ValueError

    sentences = re.split(r'[.!?][ \n]', text)
    for sentence in sentences:
        sentence_tokens = []
        for word in sentence.lower().split():
            if not word.isalpha():
                word = ''.join(filter(str.isalpha, word))
            if word:
                sentence_tokens.append(word)
        if sentence_tokens:
            sentence_tokens.append('<END>')
            tokens.extend(sentence_tokens)
    result = tuple(tokens)

    return result


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or len(word) < 1:
            raise ValueError

        if word not in self.storage:
            self.storage[word] = len(self.storage) + 1
            return len(self.storage)

        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str):
            raise ValueError

        if word not in self.storage:
            raise KeyError

        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int) or isinstance(word_id, bool):
            raise ValueError

        for word, the_id in self.storage.items():
            if the_id == word_id:
                return word

        raise KeyError

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError

        for token in corpus:
            self._put_word(token)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(text, tuple) or not isinstance(storage, WordStorage):
        raise ValueError

    text_encoded = [storage.get_id(word) for word in text]
    result = tuple(text_encoded)

    return result


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if (not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1 or
                not all(isinstance(i, int) for i in context) or any(isinstance(i, bool) for i in context)):
            raise ValueError

        for n_gram_frequency in sorted(self._n_gram_trie.n_gram_frequencies.items(), key=lambda i: i[1], reverse=True):
            if n_gram_frequency[0][:-1] == context:
                return n_gram_frequency[0][-1]
        result = sorted(self._n_gram_trie.uni_grams.items(), key=lambda i: i[1], reverse=True)

        return result[0][0][0]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError
        if not len(context) == len(self._n_gram_trie.n_grams[0]) - 1:
            raise ValueError

        halt = self._word_storage.get_id('<END>')
        sentence = list(context)
        for _ in range(19):
            sentence.append(self._generate_next_word(context))
            if sentence[-1] == halt:
                break
            context = tuple(sentence[-len(self._n_gram_trie.n_grams[0]) + 1:])
        if sentence[len(context) - 1] == halt:
            sentence = sentence[2:]
        if len(sentence) == 20 and not sentence[-1] == halt:
            sentence.append(halt)

        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        text = []

        if not isinstance(number_of_sentences, int) or not isinstance(context, tuple):
            raise ValueError

        for _ in range(number_of_sentences):
            sentence = self._generate_sentence(context)
            context = sentence[-len(self._n_gram_trie.n_grams[0]) + 1:]
            text += sentence

        return tuple(text)

    def method_one(self):
        pass


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if not isinstance(context, tuple):
            raise ValueError
        if not len(context) == len(self._n_gram_trie.n_grams[0]) - 1:
            raise ValueError

        try:
            n_gram_frequency = self._n_gram_trie.n_gram_frequencies[tuple(list(context) + [word])]
        except KeyError:
            return 0.0

        context = [str(i) for i in context]
        context = ''.join(context)
        total = 0
        for n_gram, frequency in self._n_gram_trie.n_gram_frequencies.items():
            n_gram = [str(i) for i in n_gram]
            n_gram = ''.join(n_gram)
            if context in n_gram[:-1]:
                total += frequency

        likelihood = n_gram_frequency / total

        return likelihood

    def _generate_next_word(self, context: tuple) -> int:
        max_likelihood = 0
        next_word_id = 0

        if (not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1 or
                not all(isinstance(i, int) for i in context) or any(isinstance(i, bool) for i in context) or
                any(i >= len(self._word_storage.storage) for i in context)):
            raise ValueError

        for word_id in self._word_storage.storage.values():
            likelihood = self._calculate_maximum_likelihood(word_id, context)
            if likelihood > max_likelihood:
                max_likelihood = likelihood
                next_word_id = word_id
        if not max_likelihood:
            next_word_id = sorted(self._n_gram_trie.uni_grams.items(), key=lambda i: i[1], reverse=True)[0][0][0]

        return next_word_id

    def method_one(self):
        pass


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)
        self._n_gram_tries = (n_gram_trie,) + args

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    sentence = []
    sentences = []

    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple):
        raise ValueError

    for encoded_word in encoded_text:
        if encoded_word != storage.get_id('<END>'):
            if not len(sentence):
                word = storage.get_word(encoded_word)
                sentence.append(word[0].upper() + word[1:])
            else:
                sentence.append(storage.get_word(encoded_word))
        else:
            sentences.append(' '.join(sentence))
            sentence = []
    result = tuple(sentences)

    return result


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str):
    pass

"""
Lab 4
"""

import re
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    list_tokens = []
    for some_sentences in text.split('\n'):
        sentences = re.split('[!?.] ', some_sentences)
        for sentence in sentences:
            tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()
            if tokens:
                list_tokens.extend(tokens + ['<END>'])

    return tuple(list_tokens)


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
        if not isinstance(word_id, int) or not word_id:
            raise ValueError
        if word_id not in self.storage.values():
            raise KeyError

        for word in self.storage:
            if self.storage[word] == word_id:
                return word

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
        encoded_text.append(storage.get_id(word))
    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        word_freq = 0
        max_freq_word = ''
        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if n_gram[:len(context)] == context and freq > word_freq:
                word_freq = freq
                max_freq_word = n_gram[-1]
        if not max_freq_word:
            max_freq_word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]
        return max_freq_word

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or not all(isinstance(num, int) for num in context):
            raise ValueError

        generated_sentence = list(context)
        for number in range(20):
            generated_sentence.append((self._generate_next_word(tuple(generated_sentence[-(len(context)):]))))
            if generated_sentence[-1] == self._word_storage.get_id('<END>'):
                return tuple(generated_sentence)
        if self._word_storage.get_id('<END>') not in generated_sentence:
            generated_sentence.append(self._word_storage.get_id('<END>'))
        return tuple(generated_sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        generated_text = []
        while generated_text.count(self._word_storage.get_id('<END>')) != number_of_sentences:
            new_sent = self._generate_sentence(context)
            if new_sent[len(context) - 1] == self._word_storage.get_id('<END>'):
                new_sent = new_sent[len(context):]
            generated_text.extend(list(new_sent))
            context = new_sent[-len(context):]
        return tuple(generated_text)


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        pass

    def _generate_next_word(self, context: tuple) -> int:
        pass


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    pass


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

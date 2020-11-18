"""
Language detection using n-grams
"""

import re
from math import log

# 4
def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        return ()

    result = []
    sentences = re.split('[.!?] ', text)

    for sentence in sentences:
        letters_token = []
        tokens = re.sub('[^a-z'\s']', '', sentence.lower())
        tokens = tokens.split()
        for token in tokens:
            letters_token.append(tuple(['_'] + list(token) + ['_']))
        if letters_token:
            result.append(tuple(letters_token))

    return tuple(result)

# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}

    def _put_letter(self, letter: str) -> int:
        if not isinstance(letter, str) or not 0 < len(letter) <= 1:
            return 1

        if letter not in self.storage:
            self.storage[letter] = len(self.storage)

        return 0

    def get_id_by_letter(self, letter: str) -> int:
        checks = [not isinstance(letter, str)
                  or letter not in self.storage
                  or not len(letter) > 0]

        if all(checks):
            return -1

        return self.storage[letter]

    def update(self, corpus: tuple) -> int:
        if not isinstance(corpus, tuple):
            return 1

        for sentence in corpus:
            for token in sentence:
                for letter in token:
                    self._put_letter(letter)

        return 0


# 6
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()

    encoded_corpus = []

    for sentence in corpus:
        encoded_token = []
        for token in sentence:
            encoded_token.append(tuple([storage.get_id_by_letter(letter) for letter in token]))
        encoded_corpus.append(tuple(encoded_token))

    return tuple(encoded_corpus)


# 6
class NGramTrie:

    def __init__(self, n: int):
        self.size = n
        self.n_grams = ()
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

    def fill_n_grams(self, encoded_text: tuple) -> int:
        if not isinstance(encoded_text, tuple):
            return 1

        self.n_grams = []

        for sentence in encoded_text:
            sentence_n_grams = []
            for token in sentence:
                token_n_grams = []
                for index in range(len(token) - self.size + 1):
                    n_grams = token[index:index+self.size]
                    token_n_grams.append(n_grams)
                sentence_n_grams.append(tuple(token_n_grams))
            self.n_grams.append(tuple(sentence_n_grams))
        self.n_grams = tuple(self.n_grams)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        for sentence in self.n_grams:
            for token in sentence:
                for n_gram in token:
                    self.n_gram_frequencies[n_gram] = self.n_gram_frequencies.get(n_gram, 0) + 1

        if not self.n_gram_frequencies:
            return 1

        return 0

    def calculate_log_probabilities(self) -> int:
        for n_gram in self.n_gram_frequencies:
            sum_n_grams = [self.n_gram_frequencies[l_gram] for l_gram in self.n_gram_frequencies
                           if l_gram[0] == n_gram[0]]
            self.n_gram_log_probabilities[n_gram] = log(self.n_gram_frequencies[n_gram] / sum(sum_n_grams))

        if not self.n_gram_log_probabilities:
            return 1

        return 0

    def top_n_grams(self, k: int) -> tuple:
        if not isinstance(k, int):
            return ()

        top = sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)

        return tuple(top[:k])

# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2,), top_k: int = 10):
        self.trie_levels = trie_levels
        self.top_k = top_k
        self.n_gram_storages = {}

    def new_language(self, encoded_text: tuple, language_name: str) -> int:
        checks = [not isinstance(encoded_text, tuple)
                  or not isinstance(language_name, str)
                  or None in encoded_text]

        if all(checks):
            return 1

        self.n_gram_storages[language_name] = {}

        for trie_level in self.trie_levels:
            trie = NGramTrie(trie_level)
            trie.fill_n_grams(encoded_text)
            trie.calculate_n_grams_frequencies()
            trie.calculate_log_probabilities()
            self.n_gram_storages[language_name].update({trie_level: trie})
        return 0
    
    @staticmethod
    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        checks = [not isinstance(first_n_grams, tuple)
                  or not isinstance(second_n_grams, tuple)
                  or None in first_n_grams
                  or None in second_n_grams]

        if all(checks):
            return -1

        distance = []

        for first_index, first_n_gram in enumerate(first_n_grams):
            if first_n_gram not in second_n_grams:
                distance.append(len(second_n_grams))
            for second_index, second_n_gram in enumerate(second_n_grams):
                if first_n_gram == second_n_gram:
                    distance.append(abs(first_index - second_index))
        return sum(distance)

    def detect_language(self, encoded_text: tuple) -> dict:
        if not isinstance(encoded_text, tuple):
            return {}

        language_distance = {}

        for language, storage_language in self.n_gram_storages.items():
            language_distance[language] = []
            for trie_level, n_gram_trie in storage_language.items():
                storage = NGramTrie(trie_level)
                storage.fill_n_grams(encoded_text)
                storage.calculate_n_grams_frequencies()
                language_distance[language].append(self._calculate_distance(n_gram_trie.top_n_grams(self.top_k),
                                                                            storage.top_n_grams(self.top_k)))

            language_distance[language] = sum(language_distance[language]) / len(language_distance[language])

        return language_distance

# 10
class ProbabilityLanguageDetector(LanguageDetector):

    def _calculate_sentence_probability(self, n_gram_storage: NGramTrie, sentence_n_grams: tuple) -> float:
        """
        Calculates sentence probability
        :param n_gram_storage: a filled NGramTrie with log-probabilities
        :param sentence_n_grams: n-grams from a sentence
        :return: a probability of a sentence
        """
        pass

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        pass

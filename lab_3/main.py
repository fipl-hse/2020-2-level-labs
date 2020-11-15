"""
Language detection using n-grams
"""


import math
import re
from typing import List, Tuple, Any, Dict, Optional, Callable, Union
from itertools import chain


# A good example of what would happen if you were obsessed with type annotations

# 4
def tokenize_by_sentence(text: str) -> tuple:
    """
    Splits a text into sentences, sentences into tokens, tokens into letters
    Tokens are framed with '_'
    :param text: a text
    :return: a tuple of sentence with tuples of tokens split into letters
    e.g.
    text = 'She is happy. He is happy.'
    -->  (
         (('_', 's', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_')),
         (('_', 'h', 'e', '_'), ('_', 'i', 's', '_'), ('_', 'h', 'a', 'p', 'p', 'y', '_'))
         )
    """
    if not isinstance(text, str) or not text:
        return ()

    sentences: List[str] = re.split(r'[.!?]', text)
    output: List[Tuple[tuple, ...]] = []

    for sentence in sentences:
        words: Optional[List[str]] = re.sub(r'[^a-z\s]', '', sentence.lower()).split()

        if not words:
            continue

        output.append(tuple(tuple('_' + word + '_') for word in words))

    return tuple(output)


# 4
class LetterStorage:

    def __init__(self):
        self.storage: Dict[Any, int] = {}

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str) or not 0 < len(letter) <= 1:
            return 1

        if letter not in self.storage:
            self.storage[letter]: int = len(self.storage)

        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        return self.storage.get(letter, -1)

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return 1

        while corpus and isinstance(corpus[0], tuple):
            corpus: Tuple[str, ...] = tuple(chain.from_iterable(corpus))

        for char in set(corpus):
            self._put_letter(char)

        return 0


# 6
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()

    def encode_word(word: str) -> Tuple[int, ...]:
        return tuple(storage.get_id_by_letter(char) for char in word)

    def encode_sentence(sent: tuple) -> Tuple[Tuple[int, ...], ...]:
        return tuple(encode_word(word) for word in sent)

    return tuple(encode_sentence(sentence) for sentence in corpus)


# 6
class NGramTrie:

    def __init__(self, n: int):
        self.size: int = n
        self.n_grams: tuple = ()
        self.n_gram_frequencies: Dict[Tuple[int, ...], int] = {}
        self.n_gram_log_probabilities: Dict[Tuple[int, ...], float] = {}

    def fill_n_grams(self, encoded_text: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(encoded_text, tuple):
            return 1

        def word_n_grams(word: Tuple[int, ...]) -> Tuple[int, ...]:
            for idx in range(len(word) - self.size + 1):
                yield tuple(word[idx:idx + self.size])

        def sent_n_grams(sent: tuple) -> Tuple[Tuple[int, ...]]:
            for word in sent:
                yield tuple(word_n_grams(word))

        self.n_grams = tuple(tuple(sent_n_grams(sent)) for sent in encoded_text)

        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_grams:
            return 1

        for sentence in self.n_grams:
            for word in sentence:
                for n_gram in word:
                    self.n_gram_frequencies[n_gram]: int = self.n_gram_frequencies.get(n_gram, 0) + 1

        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1

        for n_gram, freq in self.n_gram_frequencies.items():
            n_gram_prob: int = sum(_freq for token, _freq in self.n_gram_frequencies.items() if n_gram[0] == token[0])
            self.n_gram_log_probabilities[n_gram]: float = math.log(freq / n_gram_prob)

        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int):
            return ()

        freq: Dict[Tuple[int, ...], int] = self.n_gram_frequencies
        top: List[Tuple[int, ...]] = sorted(freq, key=freq.get, reverse=True)[:k]

        return tuple(top)


# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2,), top_k: int = 10):
        self.trie_levels: Tuple[int, ...] = trie_levels
        self.top_k: int = top_k
        self.n_gram_storages: Dict[str, Dict[int, NGramTrie]] = {}

    def new_language(self, encoded_text: tuple, language_name: str) -> int:
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """
        checks: List[Callable[[], bool]] = [
            lambda: isinstance(encoded_text, tuple),
            lambda: isinstance(encoded_text[0], tuple),
            lambda: isinstance(language_name, str)
        ]

        for check in checks:
            if not check():
                return 1

        self.n_gram_storages[language_name]: Dict[int, NGramTrie] = {}

        for level in self.trie_levels:
            trie: NGramTrie = NGramTrie(level)
            trie.fill_n_grams(encoded_text)
            trie.calculate_n_grams_frequencies()
            trie.calculate_log_probabilities()
            self.n_gram_storages[language_name].update({level: trie})

        return 0

    @staticmethod
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        checks: List[Callable[[], bool]] = [
            lambda: isinstance(first_n_grams, tuple),
            lambda: isinstance(second_n_grams, tuple),
            lambda: all(first_n_grams + second_n_grams)
        ]

        for check in checks:
            if not check():
                return -1

        distance: int = 0

        for idx, n_gram in enumerate(first_n_grams):
            if n_gram in second_n_grams:
                distance += abs(second_n_grams.index(n_gram) - idx)
            else:
                distance += len(second_n_grams)

        return distance

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple) or not all(encoded_text):
            return {}

        lang_distance: Dict[int, NGramTrie] = {}

        for level in self.trie_levels:
            trie_level: NGramTrie = NGramTrie(level)
            trie_level.fill_n_grams(encoded_text)
            trie_level.calculate_n_grams_frequencies()
            trie_level.calculate_log_probabilities()
            lang_distance.update({level: trie_level})

        distance: Dict[str, Union[float, List[float]]] = {}

        for language in self.n_gram_storages:

            distance[language]: List[float] = []

            for level in self.trie_levels:
                trie_unknown: NGramTrie = lang_distance[level]
                top_unknown: tuple = trie_unknown.top_n_grams(self.top_k)

                trie_level: NGramTrie = self.n_gram_storages[language][level]
                top: tuple = trie_level.top_n_grams(self.top_k)
                distance[language].append(self._calculate_distance(top, top_unknown))

        for language in distance:
            mean: float = sum(distance[language]) / len(distance[language])
            distance[language]: float = abs(mean)

        return distance


# 10
class ProbabilityLanguageDetector(LanguageDetector):

    @staticmethod
    def _calculate_sentence_probability(n_gram_storage: NGramTrie, sentence_n_grams: tuple) -> float:
        """
        Calculates sentence probability
        :param n_gram_storage: a filled NGramTrie with log-probabilities
        :param sentence_n_grams: n-grams from a sentence
        :return: a probability of a sentence
        """
        if not isinstance(sentence_n_grams, tuple) or not isinstance(n_gram_storage, NGramTrie):
            return -1.0

        probability: float = 0.0

        for word in chain.from_iterable(sentence_n_grams):
            for n_gram in word:
                if n_gram in n_gram_storage.n_gram_log_probabilities:
                    probability += n_gram_storage.n_gram_log_probabilities[n_gram]

        return probability

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        probs_dict: Dict[str, Union[float, List[float]]] = {}

        for language in self.n_gram_storages:

            probs_dict[language]: List[float] = []

            for level in self.n_gram_storages[language].values():
                probs: float = self._calculate_sentence_probability(level, encoded_text)
                probs_dict[language].append(probs)

            probs_dict[language]: float = sum(probs_dict[language]) / len(probs_dict[language])

        return probs_dict

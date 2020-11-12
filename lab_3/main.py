"""
Language detection using n-grams
"""

import re
from math import log


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
    is_text_incorrect = not isinstance(text, str) or not text
    if is_text_incorrect:
        return ()

    text = text.lower().split('. ')
    for index_sent, sentence in enumerate(text):
        sentence = re.sub(r'[^\w\s]', '', sentence).split()
        if sentence:
            for index_word, word in enumerate(sentence):
                word = '_' + word + '_'
                sentence[index_word] = tuple(word)
            text[index_sent] = tuple(sentence)
            continue
        del text[index_sent]

    return tuple(text)


# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}
        self.counter = 0

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        is_letter_incorrect = not isinstance(letter, str) or not letter
        if is_letter_incorrect:
            return 1

        if letter in self.storage:
            return 0
        self.storage[letter] = self.counter
        self.counter += 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        is_letter_incorrect = not isinstance(letter, str) or not letter
        if is_letter_incorrect or letter not in self.storage:
            return -1
        return self.storage[letter]

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        is_corpus_incorrect = not isinstance(corpus, tuple)
        if is_corpus_incorrect:
            return 1

        for sentence in corpus:
            for word in sentence:
                for letter in word:
                    self._put_letter(letter)

        return 0


# 6
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    are_args_incorrect = not isinstance(storage, LetterStorage) or not corpus or not isinstance(corpus, tuple)
    if are_args_incorrect:
        return ()

    storage.update(corpus)
    corpus_in_ids = ()
    for sentence in corpus:
        sentence_in_ids = []
        for word in sentence:
            word_in_ids = [storage.get_id_by_letter(letter) for letter in word]
            sentence_in_ids.append(tuple(word_in_ids))
        corpus_in_ids += (tuple(sentence_in_ids),)

    return corpus_in_ids


# 6
class NGramTrie:

    def __init__(self, n: int):
        self.size = n
        self.n_grams = ()
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

    def fill_n_grams(self, encoded_text: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(encoded_text, tuple):
            return 1

        for sentence in encoded_text:
            sentence_in_grams = ()
            for word in sentence:
                word_n_gram = []
                for index_letter in range(len(word)):
                    if len(word[index_letter:]) <= self.size:
                        word_n_gram.append(word[index_letter:])
                        break
                    word_n_gram.append(word[index_letter:index_letter + self.size])
                sentence_in_grams += (tuple(word_n_gram),)
            self.n_grams += (sentence_in_grams,)

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
                    if n_gram not in self.n_gram_frequencies:
                        self.n_gram_frequencies[n_gram] = 0
                    self.n_gram_frequencies[n_gram] += 1

        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        for current_n_gram in self.n_gram_frequencies:
            if current_n_gram not in self.n_gram_log_probabilities:
                n_gram_same_start = [self.n_gram_frequencies[n_gram] for n_gram in self.n_gram_frequencies
                                     if n_gram[:-1] == current_n_gram[:-1]]
                n_gram_probability = self.n_gram_frequencies[current_n_gram] / sum(n_gram_same_start)
                self.n_gram_log_probabilities[current_n_gram] = log(n_gram_probability)

        if self.n_gram_log_probabilities:
            return 0

        return 1

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not int or not isinstance(k, int) or isinstance(k, bool):
            return ()

        n_grams_frequencies_list = list(self.n_gram_frequencies.items())
        n_grams_frequencies_list.sort(key=lambda x: x[1], reverse=True)
        n_grams_top = [n_gram_frequency[0] for n_gram_frequency in n_grams_frequencies_list]

        return tuple(n_grams_top)[:k]


# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2,), top_k: int = 10):
        self.trie_levels = trie_levels
        self.top_k = top_k
        self.n_gram_storages = {}

    def new_language(self, encoded_text: tuple, language_name: str) -> int:
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """
        are_args_incorrect = (not isinstance(encoded_text, tuple) or not all(encoded_text) or
                              not language_name or not isinstance(language_name, str))
        if are_args_incorrect:
            return 1

        self.n_gram_storages[language_name] = {}
        for level in self.trie_levels:
            n_gram_trie = NGramTrie(level)
            n_gram_trie.fill_n_grams(encoded_text)
            n_gram_trie.calculate_n_grams_frequencies()
            n_gram_trie.calculate_log_probabilities()
            self.n_gram_storages[language_name][level] = n_gram_trie

        return 0

    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        are_args_incorrect = (not isinstance(first_n_grams, tuple) or not all(first_n_grams) or
                              not isinstance(second_n_grams, tuple) or not all(second_n_grams))
        if are_args_incorrect:
            return -1

        distance = ()
        for index_n_gram, n_gram in enumerate(first_n_grams):
            if n_gram in second_n_grams:
                distance += (abs(index_n_gram - second_n_grams.index(n_gram))),
                continue
            distance += (len(second_n_grams)),

        return sum(distance)

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple) or not all(encoded_text):
            return {}

        known_languages = list(self.n_gram_storages.keys())

        distances_languages = {}
        for level in self.trie_levels:
            n_grams_unknown = NGramTrie(level)
            n_grams_unknown.fill_n_grams(encoded_text)
            n_grams_unknown.calculate_n_grams_frequencies()
            for language in known_languages:
                n_grams_language = self.n_gram_storages[language][level].top_n_grams(self.top_k)
                if language not in distances_languages:
                    distances_languages[language] = []
                distances_languages[language].append(self._calculate_distance(n_grams_unknown.top_n_grams(self.top_k),
                                                                              n_grams_language))
        for language, distance_list in distances_languages.items():
            distances_languages[language] = sum(distance_list) / len(distance_list)

        return distances_languages


# 10
class ProbabilityLanguageDetector(LanguageDetector):

    def _calculate_sentence_probability(self, n_gram_storage: NGramTrie, sentence_n_grams: tuple) -> float:
        """
        Calculates sentence probability
        :param n_gram_storage: a filled NGramTrie with log-probabilities
        :param sentence_n_grams: n-grams from a sentence
        :return: a probability of a sentence
        """
        return 0

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        return {}

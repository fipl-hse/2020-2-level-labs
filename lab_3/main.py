"""
Language detection using n-grams
"""


import re
import math


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
    if not isinstance(text, str):
        return ()

    text = re.sub('[!?.]', '.', text).lower()
    text = re.sub('[^a-z .]', '', text)

    current_text = []
    for sentence in text.split('.'):
        current_sentence = []
        for word in sentence.split():
            current_word = ['_']
            for character in word:
                if character.isalpha():
                    current_word.append(character)
            current_word.append('_')
            current_sentence.append(tuple(current_word))
        current_text.append(tuple(current_sentence))
    if current_text[-1] == ():
        current_text = current_text[:-1]
    return tuple(current_text)


# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}
        self.n_size = 0

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str):
            return 1

        if letter not in self.storage:
            self.n_size += 1
            self.storage[letter] = self.n_size
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter in self.storage:
            return self.storage[letter]
        return -1

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return 1

        for sentence in corpus:
            for word in sentence:
                for character in word:
                    self._put_letter(character)
        return 0


# 6
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    if not isinstance(storage, LetterStorage) or \
            not isinstance(corpus, tuple):
        return ()

    storage.update(corpus)

    encoded_corpus = []
    for sentence in corpus:
        encoded_sentence = []
        for word in sentence:
            encoded_word = []
            for character in word:
                encoded_word.append(storage.get_id_by_letter(character))
            encoded_sentence.append(tuple(encoded_word))
        encoded_corpus.append(tuple(encoded_sentence))
    return tuple(encoded_corpus)


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

        text_ngrams = []
        for sentence in encoded_text:
            sentence_ngrams = []
            for word in sentence:
                word_ngrams = []
                for index_character in range(0, len(word)-self.size+1):
                    word_ngrams.append(tuple(word[index_character:index_character + self.size]))
                sentence_ngrams.append(tuple(word_ngrams))
            text_ngrams.append(tuple(sentence_ngrams))
        self.n_grams = tuple(text_ngrams)
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
                for ngram in word:
                    if ngram not in self.n_gram_frequencies:
                        self.n_gram_frequencies[ngram] = 1
                    else:
                        self.n_gram_frequencies[ngram] += 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1
        for ngram in self.n_gram_frequencies:
            all_counts = 0
            for another_ngram in self.n_gram_frequencies:
                if ngram[:-1] == another_ngram[:-1]:
                    all_counts += self.n_gram_frequencies[another_ngram]
            if ngram not in self.n_gram_log_probabilities:
                self.n_gram_log_probabilities[ngram] = math.log(self.n_gram_frequencies[ngram]/all_counts)
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int):
            return ()
        return tuple(sorted(self.n_gram_frequencies, reverse=True)[:k])


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
        if not isinstance(encoded_text, tuple) or not isinstance(language_name, str) or \
                None in encoded_text:
            return 1
        for trie_level in self.trie_levels:
            storage = NGramTrie(trie_level)
            storage.fill_n_grams(encoded_text)
            storage.calculate_n_grams_frequencies()
            storage.calculate_log_probabilities()

            if language_name not in self.n_gram_storages:
                self.n_gram_storages[language_name] = {trie_level: storage}
            else:
                self.n_gram_storages[language_name][trie_level] = storage
        return 0

    @staticmethod
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        if not isinstance(first_n_grams, tuple) or not isinstance(second_n_grams, tuple) or \
                None in first_n_grams or None in second_n_grams:
            return -1
        distance = 0
        for element in first_n_grams:
            if element in second_n_grams:
                distance += abs(first_n_grams.index(element)-second_n_grams.index(element))
            else:
                distance += len(second_n_grams)
        return distance

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple):
            return {}
        language_probabilities = {}
        for language, storages in self.n_gram_storages.items():
            language_probability = 0
            for ngram_level, ngram_storage in storages.items():
                storage_unknown = NGramTrie(ngram_level)
                storage_unknown.fill_n_grams(encoded_text)
                storage_unknown.calculate_n_grams_frequencies()
                top_n_grams_known_language = ngram_storage.top_n_grams(self.top_k)
                top_n_grams_unknown_language = storage_unknown.top_n_grams(self.top_k)
                language_probability += self._calculate_distance(top_n_grams_known_language,
                                                                 top_n_grams_unknown_language)
            language_probabilities[language] = language_probability / len(storages)
        return language_probabilities


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

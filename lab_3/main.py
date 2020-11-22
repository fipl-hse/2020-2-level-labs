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
    tokens = []
    sentences = text.split('.')
    for sentence in sentences:
        letters = []
        list_of_tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()
        for token in list_of_tokens:
            letters.append(tuple(['_'] + list(token) + ['_']))
        if letters:
            tokens.append(tuple(letters))
    return tuple(tokens)



# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """

        if not isinstance(letter, str) or not letter:
            return 1
        if letter not in self.storage:
            self.storage[letter] = len(self.storage) + 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """

        if not isinstance(letter, str) or not letter or letter not in self.storage:
            return -1
        return self.storage[letter]

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return 1
        for sentence in corpus:
            for token in sentence:
                for letter in token:
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
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return()
    encoded_corpus = []
    for sentence in corpus:
        encoded_sentence = []
        for token in sentence:
            encoded_token = []
            for letter in token:
                encoded_token.append(storage.get_id_by_letter(letter))
            encoded_sentence.append(tuple(encoded_token)
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
        result = []
        for sentence in encoded_text:
            sentence_gram = []
            for token in sentence:
                token_gram = []
                for element in range(len(token) - self.size + 1):
                    token_gram.append(tuple(token[element], token[i + 1]))
                sentence_gram.append(tuple(token_gram))
            result.append(tuple(sentence_gram))
        self.n_grams = tuple(result)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        for sentence in self.n_grams:
            for token in sentence:
                for element in token:
                    self.n_gram_frequencies[element] = self.n_gram_frequencies.get(element, 0) + 1
        if not self.n_gram_frequencies:
            return 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1
        for n_gram in self.n_gram_frequencies:
            appearings = 0
            for differ_n_gram in self.n_gram_frequencies:
                if n_gram[: self.size - 1] == differ_n_gram[: self.size - 1]:
                    appearings += self.n_gram_frequencies[differ_n_gram]
            probability = self.n_gram_frequencies[n_gram] / appearings
            self.n_gram_log_probabilities[n_gram] = math.log(probability)
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
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
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """
        if (not isinstance(encoded_text, tuple) or
                not isinstance(encoded_text[0], tuple) or
                not isinstance(language_name, str)):
            return 1

        self.n_gram_storages[language_name] = {}
        for trie_level in self.trie_levels:
            storage_lang = NGramTrie(trie_level)
            storage_lang.fill_n_grams(encoded_text)
            storage_lang.calculate_n_grams_frequencies()
            storage_lang.calculate_log_probabilities()
            self.n_gram_storages[language_name][trie_level] = storage_lang
        return 0

    @staticmethod
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        incorrect_inputs = (not isinstance(first_n_grams, tuple) or
                            not isinstance(second_n_grams, tuple) or
                            first_n_grams and not isinstance(first_n_grams[0], (tuple, str)) or
                            second_n_grams and not isinstance(second_n_grams[0], (tuple, str)))
        if incorrect_inputs:
            return -1

        total_distance = 0
        for ind, n_gram in enumerate(first_n_grams):
            if n_gram in second_n_grams:
                total_distance += abs(second_n_grams.index(n_gram) - ind)
            else:
                total_distance += len(second_n_grams)
        return total_distance

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple):
            return {}

        lang_distance = {}
        for language_name, storage_lang in self.n_gram_storages.items():
            lang_distance[language_name] = []
            for trie_level, n_gram_trie in storage_lang.items():
                text_storage = NGramTrie(trie_level)
                text_storage.fill_n_grams(encoded_text)
                text_storage.calculate_n_grams_frequencies()
                lang_distance[language_name].append(
                    self._calculate_distance(n_gram_trie.top_n_grams(self.top_k),
                                             text_storage.top_n_grams(self.top_k)))

            lang_distance[language_name] = sum(lang_distance[language_name]) / len(lang_distance[language_name])

        return lang_distance


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
        if not isinstance(n_gram_storage, NGramTrie) or not isinstance(sentence_n_grams, tuple):
            return -1.0

        sentence_probability = 0
        for sentence in sentence_n_grams:
            for token in sentence:
                for n_gram in token:
                    sentence_probability += n_gram_storage.n_gram_log_probabilities.get(n_gram, 0)

        return sentence_probability

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuple s of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        if not isinstance(encoded_text, tuple):
            return {}

        lang_prob_dict = {}
        for language_name in self.n_gram_storages:
            language_prob = [self._calculate_sentence_probability(n_gram_trie, encoded_text)
                             for n_gram_trie in self.n_gram_storages[language_name].values()]
            lang_prob_dict[language_name] = sum(language_prob) / len(language_prob)

        return lang_prob_dict

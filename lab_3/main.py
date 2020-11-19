"""
Language detection using n-grams
"""

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
        return tuple()

    raw_sentences = text.split('.')
    result = []
    separators = ".,?!@#$%^&*()[]<>{}-+:;/"
    for sentence in raw_sentences:
        raw_sentence = ''.join(letter for letter in sentence.lower() if letter not in separators)
        raw_words = raw_sentence.split()
        tokenized_sentence = []
        for word in raw_words:
            if word:
                word = tuple(['_'] + list(word) + ['_'])
                tokenized_sentence.append(word)
        if tokenized_sentence:
            result.append(tuple(tokenized_sentence))
    return tuple(result)


# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}
        self.count = 0

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str) or letter == '':
            return 1
        if letter not in self.storage:
            self.storage[letter] = self.count
            self.count += 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter not in self.storage:
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
    if not (isinstance(storage, LetterStorage) and isinstance(corpus, tuple)):
        return ()

    encoded_corpus = []
    for raw_sentence in corpus:
        encoded_sentence = []
        for raw_word in raw_sentence:
            encoded_word = []
            for letter in raw_word:
                encoded_word.append(storage.get_id_by_letter(letter))
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

        n_grams = []

        for raw_sentence in encoded_text:
            gram_sentence = []
            for word in raw_sentence:
                gram_word = []
                for letter_index in range(len(word)):
                    n_gram = word[letter_index:self.size + letter_index]
                    if self.size == len(n_gram):
                        gram_word.append(tuple(n_gram))
                    else:
                        gram_sentence.append(tuple(gram_word))
            n_grams.append(tuple(gram_sentence))
        self.n_grams = tuple(n_grams)

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
                    self.n_gram_frequencies[n_gram] = self.n_gram_frequencies.get(n_gram, 0) + 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        frequencies = tuple(self.n_gram_frequencies.items())

        if not frequencies:
            return 1

        for n_gram in frequencies:
            probability_coeff = 0
            for sum_item in frequencies:
                if n_gram[0][0] is sum_item[0][0]:
                    probability_coeff += sum_item[1]
            self.n_gram_log_probabilities[n_gram[0]] = math.log(n_gram[1] / probability_coeff)

        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int):
            return tuple()

        if not (k > 0 and not self.calculate_log_probabilities()):
            return tuple()

        frequencies = list(self.n_gram_frequencies.items())
        overall_top = sorted(frequencies, key=lambda x: x[1], reverse=True)
        requested_top = [n_gram[0] for n_gram in overall_top[:k]]
        
        return tuple(requested_top)

# 8
class LanguageDetector:

    def __init__(self, trie_levels: tuple = (2,), top_k: int = 10):
        pass

    def new_language(self, encoded_text: tuple, language_name: str) -> int:
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """
        pass

    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        pass

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        pass


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

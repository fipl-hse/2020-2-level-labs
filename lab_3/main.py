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
    if not isinstance(text, str) or not text:
        return ()

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z']

    check_appropriate_input = False
    for symbol in text.lower():
        if symbol in letters:
            check_appropriate_input = True
            break
    if not check_appropriate_input:
        return ()

    text = text.replace('!', '.').replace('?', '.')

    tuple_sentences = tuple(text.lower().split('. '))
    result = []

    for sentence in tuple_sentences:
        tokens = sentence.split()
        tokens_by_letter = []  # for a sentence

        for token in tokens:
            token_by_letter = ''
            for symbol in token:
                if symbol in letters:
                    token_by_letter += symbol
            token_by_letter = '_' + token_by_letter + '_'
            token_output = tuple(list(token_by_letter))
            if len(token_output) == 2:  # if token_by_letter = ('_', '_')
                continue
            tokens_by_letter.append(token_output)

        tokens_by_letter = tuple(tokens_by_letter)  # for a sentence
        result.append(tokens_by_letter)
    return tuple(result)


# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}
        self.unique_id = 0

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str) or not letter:
            return 1
        if letter in self.storage:
            return 0

        self.unique_id += 1
        self.storage[letter] = self.unique_id
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
    if not isinstance(corpus, tuple) or not isinstance(storage, LetterStorage):
        return ()

    corpus_output = []

    for sentence in corpus:
        sentence_token_id = []

        for token in sentence:
            token_id = []
            for letter in token:
                id_letter = storage.get_id_by_letter(letter)
                token_id.append(id_letter)
            token_id = tuple(token_id)
            sentence_token_id.append(token_id)

        sentence_token_id = tuple(sentence_token_id)
        corpus_output.append(sentence_token_id)
    return tuple(corpus_output)


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

        self.n_grams = []

        for sentence in encoded_text:
            sentence_with_bi_grams = []

            for token in sentence:
                token_with_bi_grams = []
                for id_unique in token[:-1]:
                    index_id = token.index(id_unique)
                    bi_gram = (token[index_id: index_id + self.size])
                    token_with_bi_grams.append(bi_gram)
                token_with_bi_grams = tuple(token_with_bi_grams)
                sentence_with_bi_grams.append(token_with_bi_grams)

            sentence_with_bi_grams = tuple(sentence_with_bi_grams)
            self.n_grams.append(sentence_with_bi_grams)
        self.n_grams = tuple(self.n_grams)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_grams:
            return 1

        for sentence in self.n_grams:
            for token in sentence:
                for bi_gram in token:
                    if bi_gram in self.n_gram_frequencies:
                        self.n_gram_frequencies[bi_gram] += 1
                    else:
                        self.n_gram_frequencies[bi_gram] = 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1

        for bi_gram_1 in self.n_gram_frequencies:
            denominator = 0
            for bi_gram_2 in self.n_gram_frequencies:
                if bi_gram_1[0] == bi_gram_2[0]:
                    denominator += self.n_gram_frequencies[bi_gram_2]
            if denominator == 0:
                denominator = 1
            probability = self.n_gram_frequencies[bi_gram_1] / denominator
            self.n_gram_log_probabilities[bi_gram_1] = math.log(probability)
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int):
            return ()

        frequencies = []
        k_bi_grams = []

        for frequency in self.n_gram_frequencies.values():
            if frequency in frequencies:
                continue
            frequencies.append(frequency)
        frequencies.sort()
        frequencies = frequencies[::-1]

        k_frequencies = frequencies[:k]
        
        for k_frequency in k_frequencies:
            for bi_gram, frequency_bi_gram in self.n_gram_frequencies.items():
                if k_frequency == frequency_bi_gram:
                    k_bi_grams.append(bi_gram)
        return tuple(k_bi_grams[:k])


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

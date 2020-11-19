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
    if not isinstance(text, str) or not text:
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
        if not isinstance(letter, str) or not letter:
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
    if not isinstance(storage, LetterStorage) or not corpus or not isinstance(corpus, tuple):
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
        text_of_n_grams = []
        for sentence in encoded_text:
            sentence_of_n_grams = []
            for token in sentence:
                token_of_n_grams = []
                for index in range(len(token)):
                    if index != len(token) - (self.size - 1):
                        n_grams = token[index:self.size + index]
                        if len(n_grams) == self.size:
                            token_of_n_grams.append(n_grams)
                if token_of_n_grams:
                    sentence_of_n_grams.append(tuple(token_of_n_grams))
            text_of_n_grams.append(tuple(sentence_of_n_grams))
        self.n_grams = tuple(text_of_n_grams)
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
        for pair in self.n_gram_frequencies:
            appearing = 0
            for begin in self.n_gram_frequencies:
                if pair[0] in begin:
                    appearing += self.n_gram_frequencies[begin]
            self.n_gram_log_probabilities[pair] = math.log(self.n_gram_frequencies[pair] / appearing)
        if not self.n_gram_log_probabilities:
            return 1
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

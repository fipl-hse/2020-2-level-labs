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
    result = []
    if not isinstance(text, str):
        return ()
    text = text.lower().split('.')
    for sentence in text:
        sentence_tokens = []
        word_tokens = ['_']
        for letter in sentence.strip():
            if letter.isalpha():
                word_tokens.append(letter)
            elif letter == ' ':
                word_tokens.append('_')
                sentence_tokens.append(tuple(word_tokens))
                word_tokens = ['_']
        word_tokens.append('_')
        sentence_tokens.append(tuple(word_tokens))
        while ('_', '_') in sentence_tokens:
            sentence_tokens.remove(('_', '_'))
        result.append(tuple(sentence_tokens))
    if result[-1] == ():
        result = result[:-1]
    return tuple(result)


# 4
class LetterStorage:

    def __init__(self):
        self.storage = {}
        pass

    def _put_letter(self, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(letter, str):
            return 1
        if len(letter) != 1:
            return 1
        if letter not in self.storage:
            self.storage[letter] = hash(letter)
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
            for word in sentence:
                for letter in word:
                    x = self._put_letter(letter)
                    if x != 0:
                        return 1
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
    encoded = []
    for sentence in corpus:
        enc_sent = []
        for word in sentence:
            enc_word = []
            for letter in word:
                enc_word.append(storage.get_id_by_letter(letter))
            if -1 in enc_word:
                return ()
            enc_sent.append(tuple(enc_word))
        encoded.append(tuple(enc_sent))
    return tuple(encoded)


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
        self.n_grams = list(self.n_grams)
        for sentence in encoded_text:
            sentence_grams = []
            for word in sentence:
                word_grams = []
                for index, letter in enumerate(word[:-1]):
                    word_grams.append(tuple(word[index: index + 2]))
                sentence_grams.append(tuple(word_grams))
            self.n_grams.append(tuple(sentence_grams))
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
            for word in sentence:
                for gram in word:
                    if gram not in self.n_gram_frequencies:
                        self.n_gram_frequencies[gram] = 1
                    else:
                        self.n_gram_frequencies[gram] += 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1
        start = {}
        for key in self.n_gram_frequencies:
            if key[0] not in start:
                start[key[0]] = self.n_gram_frequencies[key]
            else:
                start[key[0]] += self.n_gram_frequencies[key]
        for key in self.n_gram_frequencies.keys():
            if key not in self.n_gram_log_probabilities:
                self.n_gram_log_probabilities[key] = math.log(self.n_gram_frequencies[key]/start[key[0]])
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not self.n_gram_frequencies or not isinstance(k, int):
            return ()
        self.calculate_log_probabilities()
        top_ngrams = sorted(self.n_gram_log_probabilities,
                            key=lambda x: int(self.n_gram_log_probabilities[x]),
                            reverse=True)
        return tuple(top_ngrams[::-1][:k])
        pass


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

"""
Language detection using n-grams
"""
import re, math

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
    sentences = re.split('[.!?]', text)
    for sentence in sentences:
        token = re.sub('[^a-z \n]', '', sentence.lower()).split()
        token_sentence = tuple(tuple(['_'] + list(letter) + ['_']) for letter in token)
        if token_sentence:
            tokens.append(tuple(token_sentence))
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
        if letter in self.storage:
            return 0
        if not isinstance(letter, str) or not letter:
            return 1
        self.storage[letter] = len(self.storage)
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter not in self.storage:
            return -1
        return self.storage.get(letter)

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return 1
        for token in corpus:
            for word in token:
                for letter in word:
                    self._put_letter(letter)
        print(self.storage)
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
    encoded_corpus = []
    for token in corpus:
        word_numbers = []
        for word in token:
            word_numbers.append(tuple(storage.get_id_by_letter((letter)) for letter in word))
        encoded_corpus.append(tuple(word_numbers))
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
        n_gram_res = []
        for sentence in encoded_text:
            n_gram_sentence = []
            for word in sentence:
                n_gram_word = []
                for index, letter in enumerate(word[: len(word) + 1 - self.size]):
                    n_gram_word.append(tuple(word[index:index + self.size]))
                n_gram_sentence.append(tuple(n_gram_word))
            n_gram_res.append(tuple(n_gram_sentence))
        self.n_grams = tuple(n_gram_res)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(self.n_grams, tuple) or not self.n_grams:
            return 1
        for sentence in self.n_grams:
            for word in sentence:
                for num in word:
                    if self.n_gram_frequencies.get(num, False):
                        self.n_gram_frequencies[num] = self.n_gram_frequencies[num] + 1
                    else:
                        self.n_gram_frequencies[num] = 1

        return 0


    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(self.n_gram_frequencies, dict) or not self.n_gram_frequencies:
            return 1
        for n_gram in self.n_gram_frequencies:
            sum_n_gram = 0
            for n_gram_2 in self.n_gram_frequencies:
                if n_gram_2[0] == n_gram[0]:
                    sum_n_gram += self.n_gram_frequencies[n_gram_2]
            p = self.n_gram_frequencies[n_gram] / sum_n_gram
            self.n_gram_log_probabilities[n_gram] = math.log(p)
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int):
            return ()
        if k > len(self.n_gram_frequencies):
            k = len(self.n_gram_frequencies)
        top_n = []
        sort_n_grams = sorted(self.n_gram_frequencies.items(), reverse = True)
        for index in range(k):
            top_n.append(sort_n_grams[index][0])
        return tuple(top_n)


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

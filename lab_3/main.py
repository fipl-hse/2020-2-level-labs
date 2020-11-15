"""
Language detection using n-grams
"""
import re
import math


def split_into_sentences(text: str) -> tuple:
    if not isinstance(text, str):
        return ()
    for sign in ['?', '!']:
        text = text.replace(sign, '.')   # unify ending symbols
    potential_sentences = text.split('. ')
    proven_sentences = []
    solved_indexes = []  # for cases with ambuguous separation
    for index, sentence in enumerate(potential_sentences):
        if index in solved_indexes:
            continue
        try:
            if potential_sentences[index + 1][0].isupper():
                proven_sentences.append(sentence)
                continue
            solved = False
            while not solved:
                index += 1
                sentence += potential_sentences[index]
                try:
                    if potential_sentences[index + 1][0].isupper():
                        sentence = ' ' + sentence  # чтобы потом было удобно парсить слова
                        proven_sentences.append(sentence)
                        solved = True
                except IndexError:
                    proven_sentences.append(sentence)
                    solved = True
                solved_indexes.append(index)
        except IndexError:
            proven_sentences.append(sentence)
    return tuple(proven_sentences)


def tokenize_by_words(text: str) -> tuple:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    for sign in ['?', '!', '.']:
        text = text.replace(sign, ' ')
    text_output = re.sub('[^a-z \n]', '', text.lower()).split()
    return tuple(text_output)


def tokenize_by_letters(word: str) -> tuple:
    return tuple(['_'] + list(word) + ['_'])


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
    if not len(re.findall('[A-Za-z]', text)) > 0:
        return ()
    sentences = split_into_sentences(text)
    tokenized_by_words = []
    for sentence in sentences:
        tokenized_by_words.append(tokenize_by_words(sentence))
    ready_sentences = []
    for sentence in tokenized_by_words:
        tokenized_by_letters = []
        for word in sentence:
            tokenized_by_letters.append(tokenize_by_letters(word))
        ready_sentences.append(tuple(tokenized_by_letters))
    return tuple(ready_sentences)


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
        if not isinstance(letter, str):
            return 1
        if letter not in self.storage.keys():
            self.storage[letter] = len(self.storage)
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter not in self.storage.keys():
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
                    response = self._put_letter(letter)
                    if response == 1:
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
    if not (isinstance(corpus, tuple) and isinstance(storage, LetterStorage)):
        return ()
    encoded_corpus = []
    for sentence in corpus:
        encoded_sentence = []
        for word in sentence:
            encoded_word = []
            for letter in word:
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
        for sentence in encoded_text:
            grammed_sentence = []
            for word in sentence:
                grammed_word = []
                for index in range(len(word)):
                    n_gram = word[index:index + self.size]
                    if len(n_gram) == self.size:
                        grammed_word.append(tuple(n_gram))
                    else:
                        grammed_sentence.append(tuple(grammed_word))
                        continue
            n_grams.append(tuple(grammed_sentence))
        self.n_grams = tuple(n_grams)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if len(self.n_grams) == 0:
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
        items = tuple(self.n_gram_frequencies.items())
        if len(items) == 0:
            return 1
        for ngram in items:
            semi_same = 0
            for item in items:
                if item[0][0] == ngram[0][0]:
                    semi_same += item[1]
            self.n_gram_log_probabilities[ngram[0]] = math.log(ngram[1]/semi_same)
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int):
            return ()
        if not (k > 0 and self.calculate_log_probabilities() == 0):
            return ()
        frequencies = list(self.n_gram_frequencies.items())
        top = sorted(frequencies, key=lambda x: x[1], reverse=True)
        to_return = [item[0] for item in top[:k]]
        return tuple(to_return)


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
        if not (isinstance(encoded_text, tuple) and isinstance(language_name, str)):
            return 1
        if not isinstance(encoded_text[0], tuple):
            return 1
        self.n_gram_storages[language_name] = {}
        for level in self.trie_levels:
            ngram = NGramTrie(level)
            if (ngram.fill_n_grams(encoded_text) or
                ngram.calculate_n_grams_frequencies() or
                ngram.calculate_log_probabilities()):
                return 1
            self.n_gram_storages[language_name][level] = ngram
        return 0

    @staticmethod
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        if not(isinstance(first_n_grams, tuple) and isinstance(second_n_grams, tuple)):
            return -1
        if not(len(first_n_grams) > 0 and len(second_n_grams) > 0):
            return 0
        if not (isinstance(first_n_grams[0], tuple) and isinstance(second_n_grams[0], tuple)):
            return -1
        distance = 0
        for index, n_gram in enumerate(first_n_grams):
            try:
                distance += abs(index - second_n_grams.index(n_gram))
            except ValueError:
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
        if len(encoded_text) == 0:
            return {}
        if not isinstance(encoded_text[0], tuple):
            return {}
        unknown = {}
        for level in self.trie_levels:
            ngram = NGramTrie(level)
            if (ngram.fill_n_grams(
                    encoded_text) or ngram.calculate_n_grams_frequencies() or ngram.calculate_log_probabilities()):
                return 1
            unknown_top = ngram.top_n_grams(self.top_k)
            unknown[level] = unknown_top
        output = {}
        for language in self.n_gram_storages:
            distances = 0
            for level in self.n_gram_storages[language].keys():
                language_top = self.n_gram_storages[language][level].top_n_grams(self.top_k)
                distances += self._calculate_distance(unknown[level], language_top)
            average = distances / len(self.n_gram_storages[language].keys())
            output[language] = average
        return output


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
            return float(-1)
        probability = 0
        for sentence in sentence_n_grams:
            for word in sentence:
                for n_gram in word:
                    # print(n_gram)
                    # print(probability)
                    probability += n_gram_storage.n_gram_log_probabilities.get(n_gram, 0)
        return probability

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        if not isinstance(encoded_text, tuple):
            return {}
        if len(encoded_text) == 0:
            return {}
        if not isinstance(encoded_text[0], tuple):
            return {}

        output = {}
        for language in self.n_gram_storages:
            output[language] = 0
            for lvl in self.n_gram_storages[language].keys():
                first_arg = self.n_gram_storages[language][lvl]
                output[language] += self._calculate_sentence_probability(first_arg, encoded_text)
            output[language] = output[language] / len(self.trie_levels)
        return output

"""
Language detection using n-grams
"""


import math
import re

from lab_3.decorators import input_checker


# 4
@input_checker
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

    def clean_text(text):
        return re.sub('[^\.!\?\w\s]', '', text)

    def split_to_sentences(text):
        return tuple(re.findall(r'([A-Z][\w\s]+)[\.!\?]', text))

    def split_to_words(sent):
        return tuple(re.findall(r'\w+', sent.lower()))

    def split_to_chars(words):
        return tuple(tuple('_' + word + '_') for word in words)

    text = clean_text(text)
    sentences = split_to_sentences(text)
    words = (split_to_words(sent) for sent in sentences)
    tokens = (split_to_chars(word) for word in words)

    return tuple(tokens)


# 4
class LetterStorage(object):
    
    def __init__(self: object):
        self.storage = {}

    @input_checker
    def _put_letter(self: object, letter: str) -> int:
        """
        Puts a letter into storage, assigns a unique id
        :param letter: a letter
        :return: 0 if succeeds, 1 if not
        """
        if letter not in self.storage:
            self.storage[letter] = len(self.storage)
        return 0

    def get_id_by_letter(self: object, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        return self.storage.get(letter, -1)

    @input_checker
    def update(self: object, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        corpus = sum(corpus, tuple())  # flatten
        if isinstance(corpus[0], tuple):
            corpus = sum(corpus, tuple())  # flatten some more

        for char in set(corpus):
            self._put_letter(char)

        return 0


# 6
@input_checker
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """

    def encode_word(word):
        return tuple(storage.get_id_by_letter(char) for char in word)

    def encode_sentence(sent):
        return tuple(encode_word(word) for word in sent)

    def encode_text(text):
        return tuple(encode_sentence(sent) for sent in text)

    return encode_text(corpus)
  

# 6
class NGramTrie:
    
    def __init__(self: object, n: int):
        self.size = n
        self.n_grams = ()
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

    @input_checker
    def fill_n_grams(self: object, encoded_text: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        """

        def make_n_grams(i, word):
            return tuple(word[i + j] for j in range(self.size))

        def split_word_to_n_grams(word):
            return tuple(make_n_grams(i, word)
                    for i in range(len(word) - self.size + 1))

        def split_sent_to_words(sent):
            return tuple(split_word_to_n_grams(word) for word in sent)

        def split_text_to_sents(text):
            return tuple(split_sent_to_words(sent) for sent in text)
        
        self.n_grams = split_text_to_sents(encoded_text)
        return 0

    @input_checker
    def calculate_n_grams_frequencies(self: object) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_grams:
            return 1
        
        def calculate_frequencies(n_gram):
            freqs[n_gram] = freqs.get(n_gram, 0) + 1
        
        def split_word_to_n_grams(word):
            return tuple(calculate_frequencies(n_gram) for n_gram in word)

        def split_sent_to_words(sent):
            return tuple(split_word_to_n_grams(word) for word in sent)

        def split_text_to_sents(text):
            return tuple(split_sent_to_words(sent) for sent in text)

        freqs = self.n_gram_frequencies
        split_text_to_sents(self.n_grams)

        return 0

    @input_checker
    def calculate_log_probabilities(self: object) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        freqs = self.n_gram_frequencies
        if not freqs:
            return 1

        _freqs = {}  # enriched with lower-order ngram freqs
        for n_gram in freqs:
            _freqs[n_gram[:-1]] = _freqs.get(n_gram[:-1], 0) + freqs[n_gram]

        for n_gram in freqs:
            if den := _freqs.get(n_gram[:-1], 0):  # denominator
                prob = math.log(freqs[n_gram] / den)
            else:
                prob = 0
            self.n_gram_log_probabilities[n_gram] = prob
        return 0

    @input_checker
    def top_n_grams(self: object, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        freq = self.n_gram_frequencies
        if not freq:
            self.calculate_n_grams_frequencies()

        top = sorted(freq, key=freq.get, reverse=True)[:k]
        return tuple(top)


# 8
class LanguageDetector:

    def __init__(self: object,
                 trie_levels: tuple=(2,),
                 top_k: int=10):

        self.trie_levels = trie_levels
        self.top_k = top_k
        self.n_gram_storages = {}

    @input_checker
    def new_language(self: object,
                     encoded_text: tuple,
                     language_name: str) -> int:
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """
        self.n_gram_storages[language_name] = {}
        
        for n in self.trie_levels:
            trie = NGramTrie(n)
            trie.fill_n_grams(encoded_text)
            trie.calculate_n_grams_frequencies()
            trie.calculate_log_probabilities()
            self.n_gram_storages[language_name].update({n: trie})
        return 0

    @input_checker
    def _calculate_distance(self: object,
                            first_n_grams: tuple,
                            second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        second_n_grams_indexes = {n_gram: idx for idx, n_gram 
                                  in enumerate(second_n_grams)
                                  }
        dist = 0
        for idx_first, n_gram in enumerate(first_n_grams):
            if n_gram in second_n_grams:
                idx_second = second_n_grams_indexes[n_gram]
                dist += abs(idx_first - idx_second)
        return dist

    @input_checker
    def detect_language(self: object,
                        encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """

        unknown_storages = {}
        for n in self.trie_levels:
            trie = NGramTrie(n)
            trie.fill_n_grams(encoded_text)
            trie.calculate_n_grams_frequencies()
            trie.calculate_log_probabilities()
            unknown_storages.update({n: trie})

        dist = {}
        for language in self.n_gram_storages:
            dist[language] = []
            for level in self.trie_levels:
                trie_unknown = unknown_storages[level]
                top_unknown = trie_unknown.top_n_grams(self.top_k)

                trie = self.n_gram_storages[language][level]
                top = trie.top_n_grams(self.top_k)
                dist[language].append(self._calculate_distance(top, top_unknown))

        for language in dist:
            mean = sum(dist[language]) / len(dist[language])
            dist[language] = abs(mean)
        return dist


# 10
class ProbabilityLanguageDetector(LanguageDetector):

    @input_checker
    def _calculate_sentence_probability(self: object,
                                        n_gram_storage: NGramTrie,
                                        sentence_n_grams: tuple) -> float:
        """
        Calculates sentence probability
        :param n_gram_storage: a filled NGramTrie with log-probabilities
        :param sentence_n_grams: n-grams from a sentence
        :return: a probability of a sentence
        """
        prob = 0
        for sent in sentence_n_grams:
            for word in sent:
                for n_gram in word:
                    if n_gram in n_gram_storage.n_gram_log_probabilities:
                        prob += n_gram_storage.n_gram_log_probabilities[n_gram]
        return prob

    @input_checker
    def detect_language(self: object,
                        encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        prob_dict = {}
        for language in self.n_gram_storages:
            prob_dict[language] = []
            for n in self.trie_levels:
                unknown_trie = NGramTrie(n)
                unknown_trie.fill_n_grams(encoded_text)
                unknown_trie.calculate_n_grams_frequencies()
                unknown_trie.calculate_log_probabilities()

                trie = self.n_gram_storages[language][n]
                prob = self._calculate_sentence_probability(trie, unknown_trie.n_grams)
                prob_dict[language] += [prob]
        
        for language in prob_dict:
            mean = sum(prob_dict[language]) / len(prob_dict[language])
            prob_dict[language] = abs(mean)
        return prob_dict

"""
Language detection using n-grams
"""
import math
import re
from statistics import mean

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

    text = re.sub('[^a-z \n \.]', '', text.lower()).split('.')
    good_text = []

    for sentence in text:
        if sentence:
            set_of_words = sentence.split()
            good_text.append(tuple(tuple('_' + word + '_') for word in set_of_words))

    return tuple(good_text)


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

        id = 0
        if letter not in self.storage:
            self.storage[letter] = id
            id += 1

        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) and not letter in self.storage:
            return -1
        id_letter = self.storage [letter]

        return id_letter

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(corpus, tuple):
            return 1

        for word in corpus:
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
    if not isinstance(storage, LetterStorage) or not isinstance(corpus, tuple):
        return ()

    encoded_corpus = []
    for sent in corpus:     #уровень предложения
        encoded_sent = []
        for token in sent:      #уровень слова
            encoded_token = []
            for letter in token:    #буква на id
                encoded_token.append(storage.get_id_by_letter(letter))
            encoded_sent.append(tuple(encoded_token))   #закрываем уровень слова
        encoded_corpus.append(tuple(encoded_sent))
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

        list_n_gramm = []
        for sent in encoded_text:
            sent_gramm = []
            for token in sent:
                token_gramm = []
                for ind in range(len(token) - self.size + 1):   #ограничение среза
                    token_gramm.append(tuple(token[ind:ind + self.size]))   #срез по n
                sent_gramm.append(tuple(token_gramm))
            list_n_gramm.append(tuple(sent_gramm))
        self.n_grams = tuple(list_n_gramm)
        return 0


    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        for sent in self.n_grams:
            for token in sent:
                for letter in token:
                    self.n_gram_frequencies[letter] = self.n_gram_frequencies.get(letter, 0) + 1
        if not self.n_gram_frequencies:
            return 1
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_log_probabilities:
            return 1

        for elem in self.n_gram_frequencies:
            count = 0
            for other_elem in self.n_gram_frequencies:
                if elem[0] in other_elem:
                    count += self.n_gram_frequencies[other_elem]
            #натуральный логарифм от числа
            self.n_gram_log_probabilities[elem] = math.log(self.n_gram_frequencies[elem]/count)
        return 0


    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int) or k < 0 or not self.n_gram_frequencies:
            return ()

        #сортировка по убыв в функции ключа частоты
        top_list = sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)
        return tuple(top_list[:k])

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
        if not isinstance(encoded_text, tuple) or not isinstance(encoded_text[0], tuple) \
                or not isinstance(language_name, str):
            return 1

        self.n_gram_storages[language_name] = {}
        for elem in self.trie_levels:
            about_language = NGramTrie(elem)
            about_language.fill_n_grams(encoded_text)
            about_language.calculate_n_grams_frequencies()
            about_language.calculate_log_probabilities()
            self.n_gram_storages[language_name][elem] = about_language
        return 0


    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        if not isinstance(first_n_grams, tuple) or not isinstance(second_n_grams, tuple) or \
                None in first_n_grams or None in second_n_grams:
            return -1

        distance = []
        for f_ind, f_n_gram in enumerate(first_n_grams):
            if f_n_gram not in second_n_grams:
                distance.append(len(second_n_grams))
            for s_ind, s_n_gram in enumerate(second_n_grams):
                if f_n_gram == s_n_gram:
                    distance.append(abs(f_ind - s_ind))
        return sum(distance)


    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple):
            return {}

        distant_dict = {}
        for lang in self.n_gram_storages:
            dis_lang = []
            for elem in self.trie_levels:
                about_lang = NGramTrie(elem)
                about_lang.fill_n_grams(encoded_text)
                about_lang.calculate_n_grams_frequencies()
                top_elem = about_lang.top_n_grams(self.top_k)
                top_lang = self.n_gram_storages[lang][elem].top_n_grams(self.top_k)
                dis_lang.append(self._calculate_distance(top_elem,top_lang))

            distant_dict[lang] = mean(dis_lang)
            return distant_dict



# 10
class ProbabilityLanguageDetector(LanguageDetector):

    def _calculate_sentence_probability(self, n_gram_storage: NGramTrie, sentence_n_grams: tuple) -> float:
        """
        Calculates sentence probability
        :param n_gram_storage: a filled NGramTrie with log-probabilities
        :param sentence_n_grams: n-grams from a sentence
        :return: a probability of a sentence
        """
        if not isinstance(sentence_n_grams, tuple) or not isinstance(n_gram_storage, NGramTrie):
            return -1.0

        probability = 0
        for sent in sentence_n_grams:
            for word in sent:
                for n_gram in word:
                    probability += n_gram_storage.n_gram_log_probabilities.get(n_gram,0)
        return probability

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown sentence is written in using sentence probability in different languages
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary with language_name: probability
        """
        if not isinstance(encoded_text, tuple):
            return {}

        prob_dict = {}
        lang_prob = []
        for lang_name in self.n_gram_storages:
            for n_gram_trie in self.n_gram_storages[lang_name].values():
                lang_prob.append(self._calculate_sentence_probability(n_gram_trie, encoded_text))
            prob_dict[lang_name] = sum(lang_prob) / len(lang_prob)

        return prob_dict
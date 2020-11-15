"""
Language detection using n-grams
"""
import re
from math import log


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
    if not isinstance(text, str) or text == '':
        return ()

    text_outputt = re.split('[.] ', text)
    token_text = []
    for i in text_outputt:
        w_list = re.sub('[^a-z \n]', '', i.lower()).split()
        if w_list == []:
            return ()
        token_text.append(tuple(tuple(['_'] + list(w) + ['_']) for w in w_list))

    return tuple(token_text)


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
        len_storage = len(self.storage)
        if not isinstance(letter, str) or letter == '':
            return 1
        if letter not in self.storage:
            self.storage[letter] = len_storage + 1
            return 0
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter in self.storage:
            letter_id = self.storage.get(letter)
            return letter_id
        return -1

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        if isinstance(corpus, tuple):
            for w in corpus:
                for l in w:
                    self._put_letter(l)
            return 0
        return 1


# letter = LetterStorage()

# 6
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    is_inst = isinstance(corpus, tuple) or isinstance(storage, LetterStorage)
    if not is_inst:
        print(())
        return ()

    encoded_corpus = []
    sentences = []
    for s in corpus:
        if not isinstance(s, tuple):
            return ()

        for w in s:
            for l in w:
                l_id = storage.get_id_by_letter(l)
            sentences.append(tuple([l_id]))
        encoded_corpus.append(tuple(sentences))
    print(encoded_corpus)
    return tuple(encoded_corpus)

#encode_corpus(letter, corpus)

# 6
class NGramTrie:

    def __init__(self, n: int):
        self.size = n
        self.n_grams = ()
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

    encoded_text = (((1, 2, 3, 4, 5), (2, 3, 4, 5)),)
    def fill_n_grams(self, encoded_text: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(encoded_text, tuple):
            return 1
        ngram_list = []
        ngrams_sent = []
        ngrams_text = []
        for sent in encoded_text:
            for word in sent:
                for i in range(len(word) - 1):
                    ngram_list.append(tuple(word[i:i+self.size]))
                ngrams_sent.append(tuple(ngram_list))
                ngram_list = []
            ngrams_text.append(tuple(ngrams_sent))
        self.n_grams = tuple(ngrams_text)
        return 0


    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        if len(self.n_grams) == 0:
            return 1

        for sent in self.n_grams:
            for word in sent:
                for ngram in word:
                    if ngram in self.n_gram_frequencies:
                        self.n_gram_frequencies[ngram] += 1
                    else:
                        self.n_gram_frequencies[ngram] = 1
        print(self.n_gram_frequencies)
        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if len(self.n_gram_frequencies) == 0:
            return 1
        probability = {}

        for gram in self.n_gram_frequencies:
            p = self.n_gram_frequencies[gram] / sum([self.n_gram_frequencies[next_gram] for next_gram in
                                                     self.n_gram_frequencies if next_gram[0] == gram[0]])

            probability[gram] = log(p)
        self.n_gram_log_probabilities = probability
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        if not isinstance(k, int) or len(self.n_gram_frequencies) == 0:
            return ()

        most_common = sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)[:k]
        return tuple(most_common)


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

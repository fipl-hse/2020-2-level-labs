"""
Language detection using n-grams
"""
import re


def split_into_sentences(text: str) -> tuple:
    if not isinstance(text, str):
        return ()
    for sign in ['?', '!']:
        text = text.replace(sign, '.')   # unify ending symbols
    potential_sentences = text.split('. ')
    proven_sentences = []
    solved_indexes = []  # for cases with ambuguous separation
    for index, sentence in enumerate(potential_sentences):
        if index not in solved_indexes:
            try:
                if potential_sentences[index + 1][0].isupper():
                    proven_sentences.append(sentence)
                else:
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
    return tuple(['_'] + [char for char in word] + ['_'])


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
        # print(f'got sentence {corpus}')
        for sentence in corpus:
            for word in sentence:
                for letter in word:
                    # print(f'considering {letter}')
                    response = self._put_letter(letter)
                    # print(f'response is {response}')
                    if response == 1:
                        return 1
        # print(self.storage)
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
        pass

    def fill_n_grams(self, encoded_text: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        """
        pass

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        pass

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        pass

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
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

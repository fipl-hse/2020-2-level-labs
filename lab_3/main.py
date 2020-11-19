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
    if not isinstance(text, str):
        return ()

    sentences = re.split('[.!?] ', text)
    prepared_text = []

    for sentence in sentences:
        list_words = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if len(list_words) == 0:
            return ()
        prepared_text.append(tuple(tuple(['_'] + list(word) + ['_']) for word in list_words))

    return tuple(prepared_text)


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

        if letter not in self.storage:
            self.storage[letter] = len(self.storage)  # индификатор буквы -- длина storage (каждый раз другая)

        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if not isinstance(letter, str) or letter not in self.storage:
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
                    self._put_letter(letter)  # заполняем storage буквами из кортежа предложений

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

    for sentence in corpus:
        sentence_class = []
        for word in sentence:
            word_class = []
            for letter in word:
                word_class.append(storage.get_id_by_letter(letter))  # добавляем в word_class идентификаторы \
                # букв и получаем из ('a') --> (1)
            sentence_class.append(tuple(word_class))  # добавляем в sentence_class набор идентификаторов-букв \
            # и будет из ('a','b','c') --> (1,2,3)
        encoded_corpus.append(tuple(sentence_class))  # добавляем в encoded_corpus набор идентификаторов-слов

    return tuple(encoded_corpus)


# 6
class NGramTrie:

    def __init__(self, n: int):
        self.size = n  # размер грамм
        self.n_grams = ()  # тут хранятся n-граммы
        self.n_gram_frequencies = {}  # тут хранятся повторы n-грамм (например, self.n_gram_frequencies[(1,2)] = 10)
        self.n_gram_log_probabilities = {}  # тут хранятся лог-вероятность появления соответствующего кортежа в тексте

    def fill_n_grams(self, encoded_text: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        """
        if not isinstance(encoded_text, tuple):
            return 1

        bi_gram = []
        for sentence in encoded_text:
            sentence_l = []
            for word in sentence:
                word_l = []
                for i in range(len(word) - self.size + 1):  # число символов в слове минус размер н-грамм \
                    # и + 1 для индекса. так, слово (1,2,3,4) --> (4 - 2 + 1 = 3) получаем число 3
                    word_l.append(tuple((word[i], word[i + 1])))  # к списку слов присоединяем пару из индекса слова
                    # (буковки) и индекса слова но плюс один (чтобы получить пару)
                sentence_l.append(tuple(word_l))  # ну присоединяем нашу получившуюся пару в список предложений
            bi_gram.append(tuple(sentence_l))  # к нашим би-граммам добавляем все получившееся

        self.n_grams = tuple(bi_gram)

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
                    if n_gram in self.n_gram_frequencies:
                        self.n_gram_frequencies[n_gram] += 1
                    else:
                        self.n_gram_frequencies[n_gram] = 1

        return 0

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
        if not self.n_gram_frequencies:
            return 1

        for n_gram, frequency in self.n_gram_frequencies.items():
            sum_frequencies = 0  # все n-граммы, которые имеют одну и ту же n - 1 первую букву с данной n-граммой
            for n_gram1 in self.n_gram_frequencies:  # n_gram1 - интересующая наша буква
                if n_gram1[:-1] == n_gram[:-1]:
                    sum_frequencies += self.n_gram_frequencies[n_gram1]  # если совпадают, добавляем в sum_frequencies
            probability = frequency / sum_frequencies  # рассчитываем

            self.n_gram_log_probabilities[n_gram] = math.log(probability)  # логарифмируем

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
        self.trie_levels = trie_levels  # кортеж, задающий сколько нужно построить моделей NGram и какого размера
        # сюда передаётся кортеж из одного элемента `(3,)`, который означает, что
        # нужно построить одну модель NGram на основе триграм
        self.top_k = top_k  # число самых частотных n-грамм
        self.n_gram_storages = {}  # тут будут храниться заполненные `NGramTrie` для разных языков

    def new_language(self, encoded_text: tuple, language_name: str) -> int:
        """
        Fills NGramTries with regard to the trie_levels field
        :param encoded_text: an encoded text
        :param language_name: a language
        :return: 0 if succeeds, 1 if not
        """
        if (not isinstance(encoded_text, tuple) or not all(isinstance(i, tuple) for i in encoded_text)
                or not isinstance(language_name, str)):
            return 1

        self.n_gram_storages[language_name] = {}  # словарь, где ключами выступают названия языков,
        #  значения - словари, где ключами выступают размеры N-грамм из поля `trie_levels`, а значениями –
        #  заполненные `NGramTrie`.
        #  Например, после обработки английского языка с `trie_levels = (2, 3)`:
        #  self.n_gram_storages['English'] = {2: NGramTrie(2), 3: NGramTrie(3)}

        for i in self.trie_levels:
            new_language = NGramTrie(i)
            new_language.fill_n_grams(encoded_text)  # принимаем закодированный текст
            new_language.calculate_n_grams_frequencies()  # считаем повторы n-грамм
            new_language.calculate_log_probabilities()  # логарифмируем
            self.n_gram_storages[language_name][i] = new_language  # заполняем `NGramTrie` для конкретного языка
            # и добавляем в поле `self.n_gram_storages`

        return 0

    @staticmethod  # мы используем этот метод чтобы показать, что даже если в этой функции нет атрибутов класса,
    # она (функция calculate_distance) все равно должна быть в этом классе
    def _calculate_distance(first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        if ((isinstance(first_n_grams, tuple) and not first_n_grams) or
                (isinstance(second_n_grams, tuple) and not second_n_grams)):
            return 0

        if (not isinstance(first_n_grams, tuple) or not isinstance(second_n_grams, tuple)
                or not all(isinstance(i, tuple) for i in first_n_grams)
                or not all(isinstance(i, tuple) for i in second_n_grams)):
            return -1

        distance = 0

        for ind, n_gram in enumerate(first_n_grams):
            if n_gram in second_n_grams:
                distance += abs(second_n_grams.index(n_gram) - ind)  # функция abs() возвращает
                # абсолютное значение числа (т.е. всегда положительное).
                # тут мы к расстоянию прибавляем индекс определенной n-граммы из второго кортежа минус индекс
                # этой n-граммы из первого кортежа. n-грамма = (4,5) --> 4-5 = -1 --> расстояние = 1
            else:
                distance += len(second_n_grams)

        return distance

    def detect_language(self, encoded_text: tuple) -> dict:  # Функция возвращает словарь,
        # где ключом является язык, значением – расстояние.

        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        if not isinstance(encoded_text, tuple) or not all(encoded_text):
            return {}

        languages_dict = {}
        for language, dictionary in self.n_gram_storages.items():  # метод items() возвращает
            # список кортежей dict (ключ, значение)
            distances = 0
            for n_gram_size, n_gram_trie in dictionary.items():
                top_n_grams = n_gram_trie.top_n_grams(self.top_k)
                unknown_n_gram_trie = NGramTrie(n_gram_size)  # заполняем NGramTrie для неизвестного языка
                unknown_n_gram_trie.fill_n_grams(encoded_text)  # извлекаем n-граммы для неизвестного языка
                unknown_n_gram_trie.calculate_n_grams_frequencies()  # считаем повторы n-грамм для неизвестного языка
                top_n_grams1 = unknown_n_gram_trie.top_n_grams(self.top_k)  # находим топ n-граммы для н. языка
                distances += self._calculate_distance(top_n_grams, top_n_grams1)  # прибавляем к разнице высчитанную
                # разницу между топ граммами определенного языка и неизвестно языка, т.к. язык определяется
                # по расстоянию между `top_k` N-грамм.
                # Чем меньше расстояние, тем вероятнее тот или иной язык.
            languages_dict[language] = distances / len(dictionary)  # в ключ (язык) записываем усредненное значение

        return languages_dict


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

"""
Language detection using n-grams
"""
from math import log
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
    wrong_circumstances = not isinstance(text, str) or isinstance(text, bool) \
                          or text == ''
    if wrong_circumstances:
        return ()
    check = list(filter(lambda symbol: symbol.isalpha(), text))  # проверка на буквы в строке
    if check == []:
        return ()
    tokenize_text = []
    text = text.lower()  # привели к нижнему регистру
    text = text.split('. ')  # разделили на предложения
    for sentence in text:  # убираем символы
        for element in sentence:
            if element.isalpha() is False and element != ' ':
                sentence = sentence.replace(element, '')
        sentence = sentence.replace(' ', '_ _')
        sentence = '_' + sentence + '_'  # добавляем подчеркивания
        sentence = sentence.split(' ')  # разделяем на слова
        for word in sentence:  # избегаем ошибки из-за знака внутри предложения
            if len(word) <= 2:
                sentence.remove(word)
        sentence_tuple = []  # будущий кортеж предложения
        for word in sentence:  # превращаем слова в кортежи
            sentence_tuple.append(tuple(word))
        tokenize_text.append(tuple(sentence_tuple))  # добавляем кортежи предложений
    tokenize_text = tuple(tokenize_text)
    return tokenize_text


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
        wrong_circumstances = not isinstance(letter, str) or isinstance(letter, bool) \
                              or letter == '' or letter is None
        if wrong_circumstances:
            return 1
        number = 0
        if letter not in self.storage:  # записываем букву и её индекс в словарь
            self.storage[letter] = number + 1
        return 0

    def get_id_by_letter(self, letter: str) -> int:
        """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
        if letter not in self.storage:
            return -1
        return self.storage[letter]  # возвращаем индекс буквы

    def update(self, corpus: tuple) -> int:
        """
        Fills a storage by letters from the corpus
        :param corpus: a tuple of sentences
        :return: 0 if succeeds, 1 if not
        """
        wrong_circumstances = not isinstance(corpus, tuple) or isinstance(corpus, bool)
        if wrong_circumstances:
            return 1
        for sentence in corpus:
            for word in sentence:
                for symbol in word:
                   self._put_letter(symbol)
        return 0


# 6
def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Encodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: a tuple of sentences
    :return: a tuple of the encoded sentences
    """
    wrong_circumstances = not isinstance(corpus, tuple) or isinstance(corpus, bool) \
                          or not isinstance(storage, LetterStorage) or isinstance(storage, bool)
    if wrong_circumstances:
        return ()
    storage.update(corpus)  # заполнили словарь буквами предложений и присвоили им индексы
    encoded_corpus = []
    encoded_corpus_tuple = []
    for sentence in corpus:  # делаем из корпуса список со списками из строк
        encoded_sentence = []
        for word in sentence:
            encoded_sentence.append(list(word))
        encoded_corpus.append(encoded_sentence)
    for sentence in encoded_corpus:  # меняем буквы на индексы
        for word in sentence:
            for index, symbol in enumerate(word):
                    word.remove(symbol)
                    word.insert(index, storage.get_id_by_letter(symbol))
    for sentence in encoded_corpus:  # превращаем список в кортеж
        sentence_tuple = []
        for word in sentence:
            sentence_tuple.append(tuple(word))
        encoded_corpus_tuple.append(tuple(sentence_tuple))
    encoded_corpus_tuple = tuple(encoded_corpus_tuple)
    return encoded_corpus_tuple


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
        wrong_circumstances = not isinstance(encoded_text, tuple) or isinstance(encoded_text, bool)
        if wrong_circumstances:
            return 1
        n_gram_text = []
        for sentence in encoded_text:
            n_gram_sentence = []
            for word in sentence:
                n_gram_word = []
                index = 0
                while index + self.size <= len(word):  # проходимся по словам и берем нужные n-граммы
                    n_gram_word.append(word[index:index + self.size])
                    index += 1
                n_gram_sentence.append(tuple(n_gram_word))  # записываем слова в предложения
            n_gram_text.append(tuple(n_gram_sentence))  # предложения в текст
            self.n_grams = tuple(n_gram_text)
        return 0

    def calculate_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        """
        wrong_circumstances = not isinstance(self.n_grams, tuple) or isinstance(self.n_grams, bool) \
                              or self.n_grams == ()
        if wrong_circumstances:
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
        wrong_circumstances = not isinstance(self.n_gram_frequencies, dict) \
                              or isinstance(self.n_gram_frequencies, bool) \
                              or self.n_gram_frequencies == {}
        if wrong_circumstances:
            return 1
        for n_gram, freq in self.n_gram_frequencies.items():  # берем конкретный n-грамм
            frequency_large = 0  # знаменатель формулы
            if n_gram not in self.n_gram_log_probabilities:  # находим его частоту
                frequency = freq  # числитель формулы
                for key, value in self.n_gram_frequencies.items():  # берем n-граммы, отличающиеся последним элементом
                    if key[0: len(key) - 1] == n_gram[0: len(key) - 1]:
                        frequency_large += value  # складываем их частоты
            log_probability = log(frequency / frequency_large)  # находим логарифмическую вероятность
            self.n_gram_log_probabilities[n_gram] = log_probability  # записываем вероятность в словарь
        return 0

    def top_n_grams(self, k: int) -> tuple:
        """
        Gets k most common n-grams
        :return: a tuple with k most common n-grams
        """
        wrong_circumstances = not isinstance(k, int) or isinstance(k, bool) or k <= 0
        if wrong_circumstances:
            return ()
        sorted_n_grams = sorted(self.n_gram_frequencies, key=self.n_gram_frequencies.get, reverse=True)  # отсортированный список ключей по убыванию значений
        top = tuple(sorted_n_grams[0: k])  # берем нужное кол-во n-рамм
        return top


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
        wrong_circumstances = not isinstance(encoded_text, tuple) or isinstance(encoded_text, bool) \
                              or None in encoded_text or language_name == '' \
                              or not isinstance(language_name, str) or isinstance(language_name, bool)
        if wrong_circumstances:
            return 1
        dict_for_language = {}  # создаем словарь, который будет значением
        for element in self.trie_levels:  # создаем экземпляр класса NGramTrie для каждого числа
            n_g_t = NGramTrie(element)
            n_g_t.fill_n_grams(encoded_text)
            n_g_t.calculate_n_grams_frequencies()
            dict_for_language[element] = n_g_t  # записываем число в ключ, заполненный экземпляр в значение
        self.n_gram_storages[language_name] = dict_for_language  # записываем в основной словарь: язык в ключ, словарь в значение
        return 0

    def _calculate_distance(self, first_n_grams: tuple, second_n_grams: tuple) -> int:
        """
        Calculates distance between top_k n-grams
        :param first_n_grams: a tuple of the top_k n-grams
        :param second_n_grams: a tuple of the top_k n-grams
        :return: a distance
        """
        wrong_circumstances = not isinstance(first_n_grams, tuple) or isinstance(first_n_grams, bool) \
                              or not isinstance(second_n_grams, tuple) or isinstance(second_n_grams, bool) \
                              or None in first_n_grams or None in second_n_grams
        if wrong_circumstances:
            return -1
        difference = 0
        for index_1, n_gram_1 in enumerate(first_n_grams):
            if n_gram_1 not in second_n_grams:
                difference += len(second_n_grams)
            else:
                for index_2, n_gram_2 in enumerate(second_n_grams):
                    if n_gram_1 == n_gram_2:
                        difference += abs(index_1 - index_2)
        return difference

    def detect_language(self, encoded_text: tuple) -> dict:
        """
        Detects the language the unknown text is written in using the function _calculate_distance
        :param encoded_text: a tuple of sentences with tuples of tokens split into letters
        :return: a dictionary where a key is a language, a value – the distance
        """
        #text = tokenize_by_sentence(encoded_text)  # разбили текст на кортежи слов
        #storage_for_text = LetterStorage()
        #text = encode_corpus(storage_for_text, text)  # закодировали текст
        wrong_circumstances = not isinstance(encoded_text, tuple) or isinstance(encoded_text, bool)
        if wrong_circumstances:
            return {}

        final_storage = {}

        storage_for_unknown = {}  # словарь для неизвестного языка
        dict_for_unknown = {}  # создаем словарь, который будет значением
        for element in self.trie_levels:  # создаем экземпляр класса NGramTrie для каждого числа
            unknown = NGramTrie(element)
            unknown.fill_n_grams(encoded_text)
            unknown.calculate_n_grams_frequencies()
            dict_for_unknown[element] = unknown  # записываем число в ключ, заполненный экземпляр в значение
        storage_for_unknown['unknown language'] = dict_for_unknown

        # top n-граммы для неизвестного языка
        unknown_summ_all_top = []  # здесь топ n-граммы для каждого числа n
        for language, storage in storage_for_unknown.items():
            unknown_all_top = []
            for number, example in storage.items():
                top = example.top_n_grams(self.top_k)  # нашли top n-граммы для каждого экземпляра языка
                unknown_all_top.append(top)
                unknown_summ_all_top.append(tuple(unknown_all_top))

        # найти top n-граммы для каждого языка и сравнить с top n-граммами для неизвестного
        summ_all_top_english = []  # здесь топ n-граммы для каждого числа n английского
        summ_all_top_german = []  # здесь топ n-граммы для каждого числа n немецкого
        for language, storage in self.n_gram_storages.items():
            all_top = []
            for number, example in storage.items():
                top = example.top_n_grams(self.top_k)  # нашли top n-граммы для каждого экземпляра языка
                all_top.append(top)
                if language == 'English':
                    summ_all_top_english.append(tuple(all_top))
                else:
                    summ_all_top_german.append(tuple(all_top))

        # сравнить top n-граммы неизвестного языка с известными
        difference_with_english = []
        difference_with_german = []
        print(unknown_summ_all_top)
        print(summ_all_top_english)
        print(summ_all_top_german)
        for index in enumerate(unknown_summ_all_top):
            difference_e = self._calculate_distance(unknown_summ_all_top[index], summ_all_top_english[index])
            difference_g = self._calculate_distance(unknown_summ_all_top[index], summ_all_top_german[index])
            difference_with_english.append(difference_e)
            difference_with_german.append(difference_g)

        difference_with_english = mean(difference_with_english)
        difference_with_german = mean(difference_with_german)

        final_storage['English'] = difference_with_english
        final_storage['German'] = difference_with_german

        return final_storage


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

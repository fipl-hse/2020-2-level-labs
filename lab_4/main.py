"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re


def tokenize_by_sentence(text: str) -> tuple:
    wrong_type = not isinstance(text, str) or isinstance(text, bool)
    if wrong_type:
        raise ValueError
    wrong_string = list(filter(lambda symbol: symbol.isalpha(), text)) == []
    if wrong_string:
        return ()
    text = text.lower()  # переводим в нижний регистр
    text = re.split(r'[.?!][\n\s]', text)  # разделяем на предложения
    text_modernised = ''
    for sentence in text:  # удаляем ненужные символы
        for element in sentence:
            if element.isalpha() is False and element != ' ':
                sentence = sentence.replace(element, '')
        text_modernised += sentence + ' ' + '<END>' + ' '  # добавляем <END> после каждого предложения
    text_modernised = (text_modernised.split(' '))  # разделяем предложения на слова
    text_tuple = []
    for word in text_modernised:  # удаляем все ненужные элементы'
        if word != '':
            text_tuple.append(word)
    return tuple(text_tuple)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        wrong_circumstances = isinstance(word, bool) or not isinstance(word, str) or word == ''
        if wrong_circumstances:
            raise ValueError
        if word not in self.storage:
            if self.storage != {}:  # если словарь не пустой, то последнее значение словаря + 1
                all_keys = list(self.storage.keys())  # список всех ключей словаря
                self.storage[word] = self.storage[all_keys[-1]] + 1
            elif self.storage == {}:  # если словарь пустой, то идентификатор равен 1
                self.storage[word] = 1
        return self.storage[word]


    def get_id(self, word: str) -> int:
        wrong_circumstances = isinstance(word, bool) or not isinstance(word, str) or word == ''
        wrong_word = word not in self.storage
        if wrong_circumstances:
            raise ValueError
        if wrong_word:
            raise KeyError
        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        wrong_circumstances = isinstance(word_id, bool) or not isinstance(word_id, int)
        if wrong_circumstances:
            raise ValueError
        storage_values = self.storage.values()
        if word_id not in storage_values:
            raise KeyError
        for key, value in self.storage.items():
            if value == word_id:
                return key

    def update(self, corpus: tuple):
        wrong_circumstances = isinstance(corpus, bool) or not isinstance(corpus, tuple)
        if wrong_circumstances:
            raise ValueError
        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    wrong_circumstances = isinstance(text, bool) or not isinstance(text, tuple) or isinstance(storage, bool) or \
        not isinstance(storage, WordStorage)
    if wrong_circumstances:
        raise ValueError
    storage.update(text)  # присваиваем словам словаря индексы слов
    text_encoded = []
    for word in text:
        text_encoded.append(storage.get_id(word))
    text_encoded = tuple(text_encoded)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        pass

    def _generate_next_word(self, context: tuple) -> int:
        pass

    def _generate_sentence(self, context: tuple) -> tuple:
        pass

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        pass


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        pass

    def _generate_next_word(self, context: tuple) -> int:
        pass


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    pass


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

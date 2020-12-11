"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str) or text is None:
        raise ValueError

    sentences = re.split('[!?.]', text)
    list_sentences = []

    for sentence in sentences:
        new_sentence = re.sub('[^a-z \n]', '', sentence.lower()).split()
        length = len(new_sentence)
        for new_token in new_sentence:
            list_sentences.append(str(new_token))
            if new_sentence.index(new_token) == length - 1:
                list_sentences.append('<END>')
    return tuple(list_sentences)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or word is None:
            raise ValueError
        index = len(self.storage)
        if word not in self.storage:
            self.storage[word] = index
        return index

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or word is None:
            raise ValueError
        if word not in self.storage:
            raise KeyError
        else:
            return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int) or word_id is None:
            raise ValueError
        if word_id not in self.storage.values():
            raise KeyError
        words = list(self.storage.keys())
        ids = list(self.storage.values())
        index = ids.index(word_id)
        return words[index]

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple) or corpus is None:
            raise ValueError
        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple) \
            or storage is None or text is None:
        raise ValueError
    encoded_text = []
    for word in text:
        index = storage.get_id(word)
        encoded_text.append(index)
    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie
        self.context_size = self._n_gram_trie.size - 1

    def _generate_next_word(self, context: tuple) -> int:
        n_word_uni = self._n_gram_trie.uni_grams
        n_word_freq = self._n_gram_trie.n_gram_frequencies
        if not isinstance(context, tuple) or len(context) != self.context_size:
            raise ValueError

        list_n_grams = []
        for n_gram in self._n_gram_trie.n_grams:
            if context == n_gram[:self.context_size] and n_gram not in list_n_grams:
                list_n_grams.append(n_gram)

        max_value = 0
        if len(list_n_grams) == 0:
            for key, value in n_word_uni.items():
                if value > max_value:
                    max_value = value
                    needed_key = key
        else:
            for key, value in n_word_freq.items():
                for gram in list_n_grams:
                    if key == gram and value > max_value:
                        max_value = value
                        needed_key = gram
        return needed_key[-1]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        index_end = self._word_storage.get_id('<END>')
        sentence = list(context)
        counter = 0
        while counter <= 20:
            new_id = self._generate_next_word(tuple(sentence[-self.context_size:]))
            sentence.append(new_id)
            counter += 1
            if new_id == index_end:
                break
            elif counter == 21:
                sentence.append(index_end)
        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        formed_text = self._generate_sentence(context)
        counter_sent = 1
        while counter_sent != number_of_sentences:
            new_sent = self._generate_sentence(formed_text[-self.context_size:])[self.context_size + 1:]
            formed_text += new_sent
            counter_sent += 1
        return tuple(formed_text)

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

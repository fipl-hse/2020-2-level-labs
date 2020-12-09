"""
Lab 4
"""


import re
from lab_4.ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    if not text or not re.sub('[^a-z \n]', '', text.lower()):
        return ()

    sentences = re.split('[!.?]', text.lower())

    result = []
    for sentence in sentences:
        for word in re.sub('[^a-z \n]', '', sentence).split():
            result.append(word)
        result.append('<END>')
    if result[-1] == result[-2]:
        return tuple(result[:-1])
    return tuple(result)


class WordStorage:
    def __init__(self):
        self._current_id = 1
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str):
            raise ValueError
        if word not in self.storage:
            self.storage[word] = self._current_id
            self._current_id += 1
            return self.storage[word]
        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str):
            raise ValueError
        try:
            return self.storage[word]
        except KeyError:
            raise KeyError

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int):
            raise ValueError
        for key, value in self.storage.items():
            if word_id == value:
                return key
        raise KeyError

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError
        for token in corpus:
            self._put_word(token)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError
    if not text:
        return ()
    encoded_text = []
    for token in text:
        encoded_text.append(storage.get_id(token))
    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple):
            raise ValueError
        if self._n_gram_trie.size - len(context) > 1:
            raise ValueError
        unsorted_ngrams = []
        for ngram, frequency in self._n_gram_trie.n_gram_frequencies.items():
            if ngram[:-1] == context:
                unsorted_ngrams.append((frequency, ngram))
        if unsorted_ngrams:
            return sorted(unsorted_ngrams)[0][1][-1]
        return sorted(self._n_gram_trie.uni_grams.items(), key=lambda x: x[1], reverse=True)[0][0][-1]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        context = list(context)
        end = self._word_storage.get_id('<END>')
        stop_counter = 0
        while stop_counter <= 20:
            current_context = self._generate_next_word(tuple(context[-len(context):]))
            context.append(current_context)
            if context[-1] == end:
                return tuple(context)
            stop_counter += 1
        context.append(end)
        return tuple(context)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        context = list(context)
        for _ in range(number_of_sentences):
            current_context = self._generate_sentence(tuple(context[-len(context):]))
            context = current_context
        return tuple(context)

    def generate_doc(self):
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


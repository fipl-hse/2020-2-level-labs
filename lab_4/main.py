"""
Lab 4
"""

import re
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    text = re.sub(r'[^A-Za-z\n.?! ]', '', text).lower()
    text = re.sub(r'[!?.]', ' <END> ', text)

    tokens = text.split()
    if tokens and tokens[-1] != '<END>':
        tokens.append('<END>')
    return tuple(tokens)


class WordStorage:
    def __init__(self):
        self.storage = {}
        self.id_unique = 0

    def _put_word(self, word: str):
        if not isinstance(word, str):
            raise ValueError

        if word not in self.storage:
            self.id_unique += 1
            self.storage[word] = self.id_unique
        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str):
            raise ValueError
        if word not in self.storage:
            raise KeyError

        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int):
            raise ValueError
        if word_id not in self.storage.values():
            raise KeyError

        for word, id_unique in self.storage.items():
            if word_id == id_unique:
                return word

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError

        for token in corpus:
            self._put_word(token)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError

    encoded_text = []
    for token in text:
        id_token = storage.get_id(token)
        encoded_text.append(id_token)
    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie
        self.context_size = self._n_gram_trie.size - 1

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) != self.context_size:
            raise ValueError

        check_context_in_n_grams = False

        n_grams = []
        for n_gram in self._n_gram_trie.n_grams:
            if context == n_gram[:self.context_size]:
                check_context_in_n_grams = True
                n_grams.append(n_gram)

        if not check_context_in_n_grams:
            freq_uni_gram = 0
            for key, value in self._n_gram_trie.uni_grams.items():
                if value > freq_uni_gram:
                    freq_uni_gram = value
                    uni_gram = key
            return uni_gram[0]

        freq_n_gram = 0
        for key, value in self._n_gram_trie.n_gram_frequencies.items():
            for n_gram in n_grams:
                if key == n_gram and value > freq_n_gram:
                    freq_n_gram = value
                    ngram = key
        return ngram[-1]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        id_with_end = self._word_storage.get_id('<END>')

        sentence = list(context)

        attempts = 0
        while attempts < 20:
            id_in_sentence = self._generate_next_word(tuple(sentence[-self.context_size:]))
            sentence.append(id_in_sentence)
            if id_in_sentence == id_with_end:
                break
            attempts += 1
            if attempts == 20:
                sentence.append(id_with_end)
        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        text = ()
        sentence = self._generate_sentence(context)
        text += sentence
        attempts = 1
        while attempts < number_of_sentences:
            new_sentence = self._generate_sentence(sentence[-self.context_size:])[self.context_size + 1:]
            text += new_sentence
            sentence = new_sentence
            attempts += 1
        return text


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

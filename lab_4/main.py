"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re


def tokenize_by_sentence(text: str) -> tuple:

    if not isinstance(text, str):
        raise ValueError

    text_clean = re.sub(r'[^A-Za-z !?.]', '', text).lower()

    if not text_clean:
        return ()

    prepared_text = re.sub(r'[!?.$]', ' <END> ', text_clean)
    tokenized_text = prepared_text.split()

    if tokenized_text[-1] != '<END>':
        tokenized_text.append('<END>')

    return tuple(tokenized_text)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or not word:
            raise ValueError

        try:
            self.storage[word]
        except KeyError:
            self.storage[word] = len(self.storage) + 1

        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str):
            raise ValueError

        try:
            self.storage[word]
        except KeyError:
            raise KeyError
        else:
            return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if isinstance(word_id, bool) or not isinstance(word_id, int):
            raise ValueError

        if word_id not in self.storage.values():
            raise KeyError

        inverted_storage = dict([(v, k) for k, v in self.storage.items()])

        return inverted_storage[word_id]

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError

        for word in corpus:
            self._put_word(word)

        return


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError

    encoded_text = [storage.get_id(word) for word in text]

    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        most_frequent_word = ''
        word_frequency = 0

        for n_gram, n_gram_frequency in self._n_gram_trie.n_gram_frequencies.items():
            if n_gram[:-1] == context and n_gram_frequency > word_frequency:
                most_frequent_word = n_gram[-1]
                word_frequency = n_gram_frequency

        if not most_frequent_word:
            most_frequent_word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]

        return most_frequent_word

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        end_code = self._word_storage.get_id('<END>')

        if context[-1] != end_code:
            sentence = [word for word in context]
        else:
            sentence = []

        context_len = len(context)
        count = 0
        while count != 20:
            sentence.append(self._generate_next_word(context))
            context = tuple(sentence[-context_len:])
            count += 1

            if sentence[-1] == end_code:
                return tuple(sentence)

        sentence.append(end_code)
        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int)\
                or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        context_len = len(context)
        text = []

        for i in range(number_of_sentences):
            new_sentence = self._generate_sentence(context)
            text.extend(new_sentence)
            context = new_sentence[-context_len:]

        return tuple(text)


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

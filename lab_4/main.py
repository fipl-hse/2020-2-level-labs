"""
Lab 4
"""
import re
from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    sents = re.split(r'[.?!]', text)
    tokenized_sent = []

    for sent in sents:
        tokens = re.sub(r'[^a-z \n]', '', sent.lower()).split()

        if tokens:
            tokenized_sent += tokens + ['<END>']

    return tuple(tokenized_sent)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or not word:
            raise ValueError

        if word not in self.storage:
            self.storage[word] = len(self.storage) + 1

        return self.storage[word]

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or not word:
            raise ValueError

        if word not in self.storage:
            raise KeyError

        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int):
            raise ValueError

        for key, value in self.storage.items():
            if value == word_id:
                return key

        raise KeyError

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError

        for word in corpus:
            self._put_word(word)


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

        top_word = ''
        word_freq = 0

        for n_gram, n_gram_freq in self._n_gram_trie.n_gram_frequencies.items():
            if context == n_gram[:-1] and n_gram_freq > word_freq:
                top_word = n_gram[-1]
                word_freq = n_gram_freq

        if not top_word:
            top_word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]

        return top_word

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        sent = self.sent_is(context)

        for _ in range(20):
            sent.append(self._generate_next_word(context))
            context = tuple(list(context) + sent)[-len(context):]

            if sent[-1] == self._word_storage.get_id('<END>'):
                return tuple(sent)

        sent.append(self._word_storage.get_id('<END>'))

        return tuple(sent)

    def sent_is(self, context):
        if context[-1] == self._word_storage.get_id('<END>'):
            sent = []
        else:
            sent = list(context)
        return sent

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int) \
                or isinstance(number_of_sentences, bool):
            raise ValueError

        text = []

        for _ in range(number_of_sentences):
            sentence = self._generate_sentence(context)
            text.extend(sentence)
            context = tuple(text[-len(context):])

        return tuple(text)


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        type_check = [isinstance(word, int),
                      isinstance(context, tuple)]
        if not all(type_check) or word not in self._word_storage.storage.values() or \
                len([wrd for wrd in context if wrd in self._word_storage.storage.values()]) != len(context):
            raise ValueError

        wrd_freq = 0
        avrg_freq = 0
        length = self._n_gram_trie.size - 1
        for n_gram in self._n_gram_trie.n_grams:
            if context == n_gram[:length]:
                avrg_freq += 1
                if word == n_gram[-1]:
                    wrd_freq += 1

        try:
            likelihood = wrd_freq / avrg_freq
        except ZeroDivisionError:
            likelihood = 0.0
        return likelihood

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or \
                len([w for w in context if w in self._word_storage.storage.values()]) != len(context):
            raise ValueError

        next_wrd = 0
        word_freq = 0.0

        for word in self._word_storage.storage.values():
            frequency = self._calculate_maximum_likelihood(word, context)
            if frequency > word_freq:
                word_freq = frequency
                next_wrd = word

        next_word = self.if_not_freq(next_wrd, word_freq)

        return next_word

    def if_not_freq(self, next_wrd, word_freq):
        if not word_freq:
            next_wrd = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]
        return next_wrd


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple) or not encoded_text:
        raise ValueError

    decoded_text = [[]]

    for encoded_word in encoded_text:
        decoded_word = storage.get_word(encoded_word)
        if decoded_word == '<END>':
            decoded_text.append([])
        else:
            decoded_text[-1].append(decoded_word)

    decoded_text = [sentence[0][0].upper() + sentence[0][1:] + ' ' + ' '.join(sentence[1:])
                    for sentence in decoded_text if sentence]

    return tuple(decoded_text)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    elif not text:
        return ()

    # generate indexes to split
    split_indexes = []
    for index in range(len(text[:-2])):
        conditions = [not text[index].isalpha(),
                      not text[index].isdigit(),
                      text[index + 1] == " ",
                      text[index + 2].isupper()]
        if all(conditions) or text[index + 1] == "\n":
            split_indexes.append(index)

    # split text
    prev_split_point = 0
    split_text = []
    for index_split in split_indexes + [-1]:
        if index_split == -1:
            sentence = "".join([word for word in text[prev_split_point:].lower()
                                if word.isalpha() or word == " "])
        else:
            sentence = "".join([word for word in text[prev_split_point:index_split].lower()
                                if word.isalpha() or word == " "])
        if sentence:
            for word in sentence.split():
                split_text.append(word)
            split_text.append("<END>")
        prev_split_point = index_split + 2
    return tuple(split_text)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or not word:
            raise ValueError

        try:
            token = self.storage[word]
        except KeyError:
            token = len(self.storage.keys()) + 1
            self.storage[word] = token
        return token

    def get_id(self, word: str) -> int:
        if not isinstance(word, str) or not word:
            raise ValueError

        try:
            token = self.storage[word]
        except KeyError:
            raise KeyError
        return token

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int):
            raise ValueError
        reversed_storage = {value: key for key, value in self.storage.items()}
        try:
            token = reversed_storage[word_id]
        except KeyError:
            raise KeyError
        return token

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError

        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(text, tuple) or not isinstance(storage, WordStorage):
        raise ValueError

    encoded_text = []
    for word in text:
        encoded_text.append(storage.get_id(word))
    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or \
                len([w for w in context if w in self._word_storage.storage.values()]) != len(context) or\
                len(context) < self._n_gram_trie.size - 1:
            raise ValueError

        next_word = -1
        next_word_freq = 0
        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if context[:self._n_gram_trie.size-1] == n_gram[:self._n_gram_trie.size-1] and freq > next_word_freq:
                next_word_freq = freq
                next_word = n_gram[-1]
        if next_word == -1:
            uni = list(self._n_gram_trie.uni_grams.items())
            uni.sort(key=lambda x: x[1], reverse=True)
            next_word = uni[0][0][0]
        return next_word

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or \
                len([w for w in context if w in self._word_storage.storage.values()]) != len(context):
            raise ValueError

        length = len(context)
        sent = list(context)

        for _ in range(20):
            sent.append(self._generate_next_word(tuple(sent[-length:])))
            if sent[-1] == self._word_storage.get_id("<END>"):
                return tuple(sent)
        sent.append(self._word_storage.get_id("<END>"))
        return tuple(sent)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int) or\
                len([w for w in context if w in self._word_storage.storage.values()]) != len(context):
            raise ValueError

        text = []
        length = self._n_gram_trie.size - 1
        for sent_id in range(number_of_sentences):
            new_sent = self._generate_sentence(context)
            if new_sent[len(context) - 1] == self._word_storage.storage['<END>']:
                new_sent = new_sent[len(context):]
            context = new_sent[-len(context):]
            text += list(new_sent)
        return tuple(text)


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        conditions = [isinstance(word, int),
                      isinstance(context, tuple)]
        if not all(conditions) or word not in self._word_storage.storage.values() or \
                len([w for w in context if w in self._word_storage.storage.values()]) != len(context):
            raise ValueError

        word_freq = 0
        average_freq = 0
        length = self._n_gram_trie.size - 1
        for n_gram in self._n_gram_trie.n_grams:
            if context == n_gram[:length]:
                average_freq += 1
                if word == n_gram[-1]:
                    word_freq += 1

        try:
            likelihood = word_freq / average_freq
        except ZeroDivisionError:
            likelihood = 0.0
        return likelihood

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or \
                len([w for w in context if w in self._word_storage.storage.values()]) != len(context):
            raise ValueError
        next_word = -1
        word_freq = -1
        for word in self._word_storage.storage.values():
            local_freq = self._calculate_maximum_likelihood(word, context)
            if local_freq > word_freq:
                word_freq = local_freq
                next_word = word
        return next_word


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)
        self._n_gram_tries = (n_gram_trie, *args)

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or \
                len([w for w in context if w in self._word_storage.storage.values()]) != len(context):
            raise ValueError

        for trie in self._n_gram_tries:
            next_word = -1
            next_word_freq = 0
            for n_gram, freq in trie.n_gram_frequencies.items():
                if context[:trie.size - 1] == n_gram[:trie.size - 1]:
                    if freq > next_word_freq:
                        next_word_freq = freq
                        next_word = n_gram[-1]
            if next_word != -1:
                return next_word

        uni = list(self._n_gram_trie.uni_grams.items())
        uni.sort(key=lambda x: x[1], reverse=True)
        next_word = uni[0][0][0]
        return next_word


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple) or not encoded_text:
        raise ValueError

    end = storage.get_id('<END>')
    upper_condition = True
    sentence_decoded = []
    text = []

    for word_id in encoded_text:
        word = storage.get_word(word_id)
        if word_id == end:
            upper_condition = True
            text.append(" ".join(sentence_decoded))
            sentence_decoded = []
        else:
            if upper_condition:
                word = word[0].upper() + word[1:]
                upper_condition = False

            sentence_decoded.append(word)
    return tuple(text)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    # i will do it later
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    # i will do it later
    pass

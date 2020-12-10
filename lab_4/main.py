"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:

    if not isinstance(text, str):
        raise ValueError

    for sign in ['?', '!']:
        text = text.replace(sign, '.')
    sentences = text.lower().split('.')
    sentence = []
    for elem in sentences:
        if elem:
            words = elem.split()
            for word in words:
                token = ''
                for letter in word:
                    token += letter if letter.isalpha() else ''
                if len(token) != 0:
                    sentence.append(token)
            if len(sentence) != 0:
                sentence.append('<END>')
    return tuple(sentence)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):

        if not isinstance(word, str) or len(word) == 0:
            raise ValueError

        if word not in self.storage:
            self.storage[word] = 5 + len(self.storage)
        return self.storage[word]

    def get_id(self, word: str) -> int:

        if not isinstance(word, str) or len(word) == 0:
            raise ValueError

        if word not in self.storage:
            raise KeyError

        return self.storage[word]

    def get_word(self, word_id: int) -> str:

        if not isinstance(word_id, int) or word_id <= 0:
            raise ValueError
        for word, _id in self.storage.items():
            if word_id == _id:
                return word
        raise KeyError

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

        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1 or not context:
            raise ValueError
        common = []
        for n_gram in self._n_gram_trie.n_grams:
            if context == n_gram[:len(context)]:
                common.append(n_gram)
        if common:
            top = sorted(common, key=self._n_gram_trie.n_gram_frequencies.get, reverse=True)
            return top[0][-1]
        top = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
        return top[0][0]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        g_sentence = list(context[:self._n_gram_trie.size - 1])

        for _ in range(20):
            tu = tuple(g_sentence[-(self._n_gram_trie.size - 1):])
            g_sentence.append(self._generate_next_word(tu))

            if self._word_storage.get_id('<END>') in g_sentence[:-len(context)]:
                g_sentence = g_sentence[g_sentence.index(self._word_storage.get_id('<END>')) + 1:]

            if g_sentence[-1] == self._word_storage.get_id('<END>'):
                break

        if self._word_storage.get_id('<END>') not in g_sentence:
            g_sentence.append(self._word_storage.get_id('<END>'))
        return tuple(g_sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:

        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int) or not context \
                or number_of_sentences <= 0:
            raise ValueError

        gen_text = []

        for _ in range(number_of_sentences):
            gen_sentence = self._generate_sentence(context)
            context = gen_sentence[-(self._n_gram_trie.size - 1):]
            gen_text.extend(list(gen_sentence))

        return tuple(gen_text)


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:

        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        c_freq = 0.0
        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if n_gram[:len(context)] == context:
                c_freq += freq
        if c_freq:
            return self._n_gram_trie.n_gram_frequencies.get(context + (word,), 0) / c_freq
        else:
            return c_freq

    def _generate_next_word(self, context: tuple) -> int:

        if not isinstance(context, tuple) or not context or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        for word in context:
            if word not in self._word_storage.storage.values():
                raise ValueError

        likelihood_dict = {}
        for word in self._word_storage.storage.values():
            likelihood_dict[word] = self._calculate_maximum_likelihood(word, context)
        if likelihood_dict:
            top = sorted(likelihood_dict, key=likelihood_dict.get, reverse=True)
            return top[0]
        top = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
        return top[0][0]


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:

    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple):
        raise ValueError
    sentence = []
    sentences = []
    for encoded_word in encoded_text:
        if encoded_word != storage.get_id('<END>'):
            if len(sentence) == 0:
                word = storage.get_word(encoded_word)
                sentence.append(word[0].upper() + word[1:])
            else:
                sentence.append(storage.get_word(encoded_word))
        else:
            sentences.append(' '.join(sentence))
            sentence = []
    return tuple(sentences)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

"""
Lab 4
"""


from ngrams.ngram_trie import NGramTrie

import re

def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    if not text:
        return ()

    tokens = []
    sentences = re.split(r'[.!?]', text)

    for sentence in sentences:
        splited_sent = re.sub(r'[^a-z \n]', '', sentence.lower()).split()
        if splited_sent:
            tokens += splited_sent + ['<END>']
    return tuple(tokens)

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

        if word_id not in self.storage.values():
            raise KeyError

        for word, id in self.storage.items():
            if id == word_id:
                return word


    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError

        for word in corpus:
            self._put_word(word)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError

    encoded_text = []

    for word in text:
        encoded_text += [storage.get_id(word)]
    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or not context or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        most_freq_word = ''
        word_frequency = 0

        for n_gram, n_gram_freq in self._n_gram_trie.n_gram_frequencies.items():
            if n_gram[:len(context)] == context and n_gram_freq > word_frequency:
                word_frequency = n_gram_freq
                most_freq_word = n_gram[-1]
        if not most_freq_word:
            return max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]

        return most_freq_word

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        sentence = list(context)

        for _ in range(20):
            sentence += [self._generate_next_word(tuple(sentence[-len(context):]))]
            if sentence[-1] == self._word_storage.get_id("<END>"):
                return tuple(sentence)
        sentence += [self._word_storage.get_id("<END>")]
        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int) or not context:
            raise ValueError

        generated_text = []

        for _ in range(number_of_sentences):
            generated_sentence = self._generate_sentence(context)
            if generated_sentence[len(context) - 1] == self._word_storage.storage['<END>']:
                generated_sentence = generated_sentence[len(context):]
            generated_text.extend(generated_sentence)
            context = tuple(generated_text[-len(context):])
        return tuple(generated_text)

class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if not isinstance(word, int) or not isinstance(context, tuple) or not context \
                or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        freq_context = 0.0
        for n_gram, n_gram_freq in self._n_gram_trie.n_gram_frequencies.items():
            if n_gram[:len(context)] == context:
                freq_context += n_gram_freq
        if freq_context:
            freq_context = self._n_gram_trie.n_gram_frequencies.get(tuple(context + (word,)), 0) / freq_context
        return freq_context

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size or \
                context[0] > len(self._word_storage.storage):
            raise ValueError

        word_freq = 0
        next_word = 0

        for word in self._word_storage.storage.values():
            frequency = self._calculate_maximum_likelihood(word, context)
            if frequency > word_freq:
                word_freq = frequency
                next_word = word
        if not word_freq:
            next_word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]
        return next_word

class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)
        self._n_gram_tries = (n_gram_trie,) + args

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or not context \
                or [word for word in context if word not in self._word_storage.storage.values()]:
            raise ValueError

        next_word = ''
        word_freq = 0

        for n_gram_trie in self._n_gram_tries:
            for n_gram, n_gram_freq in n_gram_trie.n_gram_frequencies.items():
                if n_gram[:-1] == context and n_gram_freq > word_freq:
                    next_word = n_gram[-1]
                    word_freq = n_gram_freq
        if not next_word:
            next_word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]
        return next_word


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple) or not encoded_text:
        raise ValueError

    decoded_text = []
    decoded_sent = []

    for encoded_word in encoded_text:
        if encoded_word != storage.get_id('<END>'):
            if len(decoded_sent) == 0:
                decoded_word = storage.get_word(encoded_word)
                decoded_sent += [decoded_word[0].upper() + decoded_word[1:]]
            else:
                decoded_sent += [(storage.get_word(encoded_word))]
        else:
            decoded_text += [' '.join(decoded_sent)]
            decoded_sent = []
    return tuple(decoded_text)

def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

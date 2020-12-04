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

    text_splited = re.split('[!?.]', text)
    new_text = []

    for sentence in text_splited:
        if len(sentence.strip()):
            list_tokens = re.sub('[^a-z \n]', '', sentence.lower()).split()
            if len(list_tokens):
                list_tokens += ['<END>']
                new_text.append(list_tokens)

    output = []

    for sentence in new_text:
        for element in sentence:
            output.append(element)

    return tuple(output)


class WordStorage:
    def __init__(self):
        self.storage = {}
        self.id = 1

    def _put_word(self, word: str):

        if not isinstance(word, str):
            raise ValueError

        if word not in self.storage:
            self.storage[word] = self.id
            self.id += 1

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

        for key, word_id_another in self.storage.items():
            if word_id == word_id_another:
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

    encoded_corpus = []
    for word in text:
        word_id = storage.get_id(word)
        encoded_corpus.append(word_id)

    return tuple(encoded_corpus)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:

        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        max_frequency = 0
        full_context = ()

        for key, frequency in self._n_gram_trie.n_gram_frequencies.items():
            if key[:len(context)] == context and frequency > max_frequency:
                max_frequency = frequency
                full_context = key

        if not full_context:
            return max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]

        return full_context[-1]

    def _generate_sentence(self, context: tuple) -> tuple:

        if not isinstance(context, tuple):
            raise ValueError

        sentence_generated = list(context)
        for i in range(20):
            sentence_generated.append(self._generate_next_word(tuple(sentence_generated[-(len(context)):])))
            if sentence_generated[-1] == self._word_storage.storage['<END>']:
                break

        else:
            sentence_generated.append(self._word_storage.storage['<END>'])
        return tuple(sentence_generated)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:

        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError

        text_generated = []

        for i in range(number_of_sentences):
            new_sentence = self._generate_sentence(context)
            if new_sentence[len(context) - 1] == self._word_storage.storage['<END>']:
                new_sentence = new_sentence[len(context):]
            text_generated.extend(new_sentence)

        return tuple(text_generated)


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

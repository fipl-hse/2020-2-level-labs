"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError

    sentences = re.split(r'[.!?]', text)
    res = []

    for sentence in sentences:
        clean_sentence = re.sub('[^a-z \n]', '', sentence.lower()).split()
        if clean_sentence:
            res.extend(clean_sentence + ['<END>'])

    return tuple(res)


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
        for word in self.storage:
            if self.storage[word] == word_id:
                return word

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError
        for word in corpus:
            self._put_word(word)
        return 0


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError

    return tuple([storage.get_id(word) for word in text])


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError

        context_n_grams = {}
        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if context == n_gram[:self._n_gram_trie.size - 1]:
                context_n_grams[n_gram] = freq

        if not context_n_grams:
            finding_top_word = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
            return finding_top_word[0][0]

        finding_top_context_n_gram = sorted(context_n_grams, key=context_n_grams.get, reverse=True)
        return finding_top_context_n_gram[0][-1]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError

        new_context = []
        new_context.extend(list(context))
        counter = 0
        while counter < 20:
            counter += 1
            new_context.append(self._generate_next_word(tuple(new_context[-len(context):])))
            if new_context[-1] == self._word_storage.storage['<END>']:
                break
        else:
            new_context.append(self._word_storage.storage['<END>'])
        return tuple(new_context)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int) \
                or isinstance(number_of_sentences, bool):
            raise ValueError

        text = []
        while number_of_sentences:
            number_of_sentences -= 1
            new_sentence = self._generate_sentence(context)

            if new_sentence[len(context) - 1] == self._word_storage.storage['<END>']:
                new_sentence = new_sentence[len(context):]
            text.extend(new_sentence)
            context = tuple(text[-len(context):])
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

"""
Lab 4
"""
import re

from ngrams.ngram_trie import NGramTrie


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    if not text:
        return ()
    if text[-1] in '.!?':
        text = text[:-1]
    new_text = ''
    for sign in text:
        if re.match(r'[a-zA-Z.?! ]', sign):
            new_text += sign
        elif re.match(r'\n', sign):
            new_text += ' '
    if not new_text:
        return ()
    sentences = re.split(r'[.!?] ', new_text)
    list_words = []
    for sentence in sentences:
        sentence = sentence.lower()
        sentence += ' <END>'
        sentence = sentence.split()
        list_words.extend(sentence)
    return tuple(list_words)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or not word:
            raise ValueError
        if word not in self.storage:
            self.storage[word] = len(self.storage) + 1
        return len(self.storage)

    def get_id(self, word: str) -> int:
        if not isinstance(word, str):
            raise ValueError
        if word not in self.storage.keys():
            raise KeyError
        return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int):
            raise ValueError
        if word_id not in self.storage.values():
            raise KeyError
        for key, value in self.storage.items():
            if value == word_id:
                return key

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError
        for word in corpus:
           self._put_word(word)



def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(text, tuple):
        raise ValueError
    result = tuple([storage.get_id(word) for word in text])
    return result


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError
        new_dict = {}
        for key, value in self._n_gram_trie.n_gram_frequencies.items():
            if context == key[:-1]:
                new_dict[key] = value
        for key, value in new_dict.items():
            if value == max(new_dict.values()):
                return key[-1]
        for key, value in self._n_gram_trie.uni_grams.items():
            if value == max(self._n_gram_trie.uni_grams.values()):
                return key[0]

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError
        sentence = list(context)
        counter = 0
        while counter != 20:
            next_word_id = self._generate_next_word(tuple(sentence[-self._n_gram_trie.size + 1:]))
            sentence.append(next_word_id)
            if self._word_storage.get_word(next_word_id) == '<END>':
                return tuple(sentence)
            counter += 1
        sentence.append(self._word_storage.get_id('<END>'))
        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int):
            raise ValueError
        text = []
        sentence = context
        for x in range(number_of_sentences):
            sentence = self._generate_sentence(sentence)
            text.extend(sentence)
            sentence = sentence[-self._n_gram_trie.size + 1:]
        return tuple(text)


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if not isinstance(word, int) or word not in self._word_storage.storage.values() \
                or not isinstance(context, tuple):
            raise ValueError
        for value in context:
            if value not in self._word_storage.storage.values():
                raise ValueError
        n_gram = list(context)
        n_gram.append(word)
        n_gram_number = 0
        n_gram_freq = 0
        if tuple(n_gram) in self._n_gram_trie.n_gram_frequencies.keys():
            n_gram_freq = self._n_gram_trie.n_gram_frequencies[tuple(n_gram)]
        for key, value in self._n_gram_trie.n_gram_frequencies.items():
            if key[:-1] == context:
                n_gram_number += value
        if n_gram_number == 0:
            return 0
        return n_gram_freq/n_gram_number


    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple):
            raise ValueError
        for word in context:
            if word not in self._word_storage.storage.values():
                raise ValueError
        freq_dict = {value: self._calculate_maximum_likelihood(value, context) for value in self._word_storage.storage.values()}
        for key, value in freq_dict.items():
            if value == max(freq_dict.values()):
                return key


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    result = []
    for word in encoded_text:
        result.append(storage.get_word(word))
    

def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

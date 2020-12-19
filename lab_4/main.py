"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    list_tokens = []
    sentences = re.split('[!?.]', text)
    for sentence in sentences:
        new_sentence = re.sub('[^a-z \n]', '', sentence.lower()).split()
        length = len(new_sentence)
        for token in new_sentence:
            list_tokens.append(str(token))
            if new_sentence.index(token) == length - 1:
                list_tokens.append('<END>')
    return tuple(list_tokens)



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
        else:
            return self.storage[word]

    def get_word(self, word_id: int) -> str:
        if not isinstance(word_id, int) or not word_id:
            raise ValueError
        if word_id not in self.storage.values():
            raise KeyError
        words = list(self.storage.keys())
        ids = list(self.storage.values())
        index = ids.index(word_id)
        return words[index]

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
        encoded_text.append(storage.get_id(word))
    return tuple(encoded_text)


class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        if not isinstance(context, tuple) or len(context) != self._n_gram_trie.size - 1:
            raise ValueError
        freq_cont = {}
        for n_gram, freq in self._n_gram_trie.n_gram_frequencies.items():
            if context == n_gram[:self._n_gram_trie.size - 1]:
                freq_cont[n_gram] = freq
        if not freq_cont:
            top_n_gram = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=False)
            return top_n_gram[-1][-1]
        top_context_n_gram = sorted(freq_cont, key=freq_cont.get, reverse=False)
        return top_context_n_gram[-1][-1]




    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError
        list_cont = list(context)
        for i in range(20):
            word = self._generate_next_word(context)
            list_cont.append(word)
            if list_cont[-1] == self._word_storage.storage['<END>']:
                break
        else:
            list_cont.append(self._word_storage.storage['<END>'])
        return tuple(list_cont)



    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int) \
                or isinstance(number_of_sentences, bool):
            raise ValueError

        text = []
        for i in range(number_of_sentences):
            new_sentence = self._generate_sentence(context)

            if new_sentence[len(context) - 1] == self._word_storage.storage['<END>']:
                new_sentence = new_sentence[len(context):]
            text.extend(new_sentence)
            context = tuple(text[-len(context):])
        return tuple(text)


class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if not isinstance(context, tuple) or not isinstance(word, int) or not context \
                or len(context) != self._n_gram_trie.size - 1:
            raise ValueError
        word_freq = 0.0
        for key, frequency in self._n_gram_trie.n_gram_frequencies.items():
            if key[:len(context)] == context:
                word_freq += frequency
        if word_freq:
            word_freq = self._n_gram_trie.n_gram_frequencies.get(tuple(list(context) + [word]), 0) / word_freq
        return word_freq

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or not context or len(context) != self._n_gram_trie.size - 1:
            raise ValueError
        for element in context:
            if element not in self._word_storage.storage.values():
                raise ValueError
        likelihood_dict = {}
        for element in self._word_storage.storage.values():
            likelihood_dict[element] = self._calculate_maximum_likelihood(element, context)
        if likelihood_dict:
            top = sorted(likelihood_dict, key=likelihood_dict.get, reverse=True)
            return top[0]
        top = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
        return top[0][0]


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)
        self._n_gram_tries = (n_gram_trie, ) + args

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or not context:
            raise ValueError
        for word in context:
            if word not in self._word_storage.storage.values():
                raise ValueError
        tries_sorted = sorted(list(self._n_gram_tries), key=lambda n_gram_trie: n_gram_trie.size, reverse=True)
        for trie in tries_sorted:
            beg = []
            for n_gram in trie.n_grams:
                if n_gram[:trie.size - 1] == context[:trie.size - 1]:
                    beg.append(n_gram)
            if beg:
                top = sorted(beg, key=trie.n_gram_frequencies.get, reverse=True)
                return top[0][-1]
        top = sorted(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get, reverse=True)
        return top[0][0]



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
    if not isinstance(model, NGramTextGenerator) or not isinstance(path_to_saved_model, str):
        raise ValueError


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    if not isinstance(path_to_saved_model, str):
        raise ValueError

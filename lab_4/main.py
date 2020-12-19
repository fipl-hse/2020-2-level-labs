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

        frequent_word = ''
        word_frequency = 0
        for n_gram, n_gram_frequency in self._n_gram_trie.n_gram_frequencies.items():
            if n_gram[:-1] == context and n_gram_frequency > word_frequency:
                frequent_word = n_gram[-1]
                word_frequency = n_gram_frequency
        if not frequent_word:
            frequent_word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]
        return frequent_word

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple) or len(context) + 1 != self._n_gram_trie.size:
            raise ValueError

        end_code = self._word_storage.get_id('<END>')
        if context[-1] == end_code:
            sentence = []
        else:
            sentence = list(context)
        context_len = len(context)
        count = 0
        while count != 20:
            sentence.append(self._generate_next_word(context))
            context = tuple(list(context) + sentence)[-context_len:]
            count += 1
            if sentence[-1] == end_code:
                if len(sentence) == 1:
                    uni_grams_no_end = list(self._n_gram_trie.uni_grams.keys())
                    uni_grams_no_end.remove((end_code,))
                    sentence = random.choices(uni_grams_no_end, k=5) + [(end_code,)]
                    return tuple(word_id[0] for word_id in sentence)

                return sentence
        sentence.append(end_code)
        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(context, tuple) or not isinstance(number_of_sentences, int) or not context:
            raise ValueError
        generated_text = []
        for element in range(number_of_sentences):
            generated_sentence = self._generate_sentence(context)
            context = generated_sentence[-(self._n_gram_trie.size - 1):]
            generated_text.extend(list(generated_sentence))
        return tuple(generated_text)


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
        self._n_gram_tries = (n_gram_trie, *args)

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple) or not context:
            raise ValueError
        for word in context:
            if word not in self._word_storage.storage.values():
                raise ValueError
        freq_word = ''
        word_frequency = 0
        for n_gram_trie in self._n_gram_tries:
            for n_gram, n_gram_frequency in n_gram_trie.n_gram_frequencies.items():
                if n_gram[:-1] == context and n_gram_frequency > word_frequency:
                    freq_word = n_gram[-1]
                    word_frequency = n_gram_frequency
        if not freq_word:
            freq_word = max(self._n_gram_trie.uni_grams, key=self._n_gram_trie.uni_grams.get)[0]
        return freq_word


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    if not isinstance(storage, WordStorage) or not isinstance(encoded_text, tuple):
        raise ValueError
    text = []
    sentence = []
    for element in encoded_text:
        if element != storage.get_id('<END>'):
            if len(sentence) == 0:
                word = storage.get_word(element)
                sentence.append(word[0].upper() + word[1:])
            else:
                sentence.append((storage.get_word(element)))
        else:
            text.append(' '.join(sentence))
            sentence = []
    return tuple(text)


def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

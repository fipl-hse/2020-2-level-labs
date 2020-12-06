"""
Lab 4
"""

from ngrams.ngram_trie import NGramTrie
import re

def split_into_sentences(text: str) -> tuple:
    if not isinstance(text, str):
        return ()
    for sign in ['?', '!']:
        text = text.replace(sign, '.')   # unify ending symbols
    potential_sentences = re.split('\.\\s', text)
    proven_sentences = []
    solved_indexes = []  # for cases with ambuguous separation
    for index, sentence in enumerate(potential_sentences):
        if index in solved_indexes:
            continue
        try:
            if potential_sentences[index + 1][0].isupper():
                proven_sentences.append(sentence)
                continue
            solved = False
            while not solved:
                index += 1
                sentence += potential_sentences[index]
                try:
                    if potential_sentences[index + 1][0].isupper():
                        sentence = ' ' + sentence  # чтобы потом было удобно парсить слова
                        proven_sentences.append(sentence)
                        solved = True
                except IndexError:
                    proven_sentences.append(sentence)
                    solved = True
                solved_indexes.append(index)
        except IndexError:
            proven_sentences.append(sentence)
    return tuple(proven_sentences)


def tokenize_by_words(text: str) -> tuple:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    for sign in ['?', '!', '.']:
        text = text.replace(sign, ' ')
    text_output = re.sub('[^a-z \n]', '', text.lower()).split() + ['<END>']
    return text_output


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text, str):
        raise ValueError
    if not len(re.findall('[A-Za-z]', text)) > 0:
        return ()
    sentences = split_into_sentences(text)
    tokenized = [tokenize_by_words(sentence) for sentence in sentences]
    result = []
    for sentence in tokenized:
        result += sentence
    return tuple(result)


class WordStorage:
    def __init__(self):
        self.storage = {}

    def _put_word(self, word: str):
        if not isinstance(word, str) or len(word) < 1:
            raise ValueError
        if word not in self.storage:
            self.storage[word] = len(self.storage) + 1
            return len(self.storage)
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
        if word_id not in self.storage.values():
            raise KeyError
        for key in self.storage.keys():
            if self.storage[key] == word_id:
                return key

    def update(self, corpus: tuple):
        if not isinstance(corpus, tuple):
            raise ValueError
        for token in corpus:
            self._put_word(token)


def encode_text(storage: WordStorage, text: tuple) -> tuple:
    if not isinstance(text, tuple) or not isinstance(storage, WordStorage):
        raise ValueError
    encoded = [storage.get_id(word) for word in text]
    return tuple(encoded)




class NGramTextGenerator:
    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie):
        '''
        _word_storage is a dictionary { word : word_id }
        trie includes arguments:
        trie.n_grams - size of ngrams
        trie.n_gram_frequencies - {ngram : frequency}
        trie.uni_grams - {unigram : frequency)
        '''
        self._word_storage = word_storage
        self._n_gram_trie = n_gram_trie

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple):
            raise ValueError
        if not len(context) == len(self._n_gram_trie.n_grams[0]) - 1:
            raise  ValueError
        context = [str(i) for i in context]
        context = ''.join(context)
        chosen = []
        for ngram, freq in self._n_gram_trie.n_gram_frequencies.items():
            ngram = [str(i) for i in ngram]
            ngram = ''.join(ngram)
            if context in ngram[:-1]:
                chosen.append((ngram[-1], freq))
        if len(chosen) > 0:
            chosen.sort(key=lambda x: x[1], reverse=True)
            return int(chosen[0][0])
        unis =  list(self._n_gram_trie.uni_grams.items())
        unis.sort(key=lambda x: x[1], reverse=True)
        return int(unis[0][0][0])

    def _generate_sentence(self, context: tuple) -> tuple:
        if not isinstance(context, tuple):
            raise ValueError
        if not len(context) == len(self._n_gram_trie.n_grams[0]) - 1:
            print(context)
            print(len(self._n_gram_trie.n_grams[0]))
            raise ValueError
        stop_word = self._word_storage.get_id('<END>')
        sentence = [context[0]]
        for _ in range(19):
            sentence.append(self._generate_next_word(context))
            if sentence[-1] == stop_word:
                break
            context = tuple(sentence[-len(self._n_gram_trie.n_grams[0]) + 1:])
        if len(sentence) == 20 and not sentence[-1] == stop_word:
            sentence.append(stop_word)
        return tuple(sentence)

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        if not isinstance(number_of_sentences, int) or not isinstance(context, tuple):
            raise ValueError
        context_length = len(context) + 1
        text = []
        for _ in range(number_of_sentences):
            print('GENERATE TEXT', context)
            sentence = self._generate_sentence(context)
            print(sentence)
            context = sentence[-len(self._n_gram_trie.n_grams[0]):-1]
            print(-len(self._n_gram_trie.n_grams[0]) + 2)
            text += sentence
        return text



class LikelihoodBasedTextGenerator(NGramTextGenerator):

    def _calculate_maximum_likelihood(self, word: int, context: tuple) -> float:
        if not isinstance(context, tuple):
            raise ValueError
        if not len(context) == len(self._n_gram_trie.n_grams[0]) - 1:
            raise  ValueError
        try:
            ngram_freq = self._n_gram_trie.n_gram_frequencies[tuple(list(context) + [word])]
        except KeyError:
            return 0.0
        context = [str(i) for i in context]
        context = ''.join(context)
        total = 0
        for ngram, freq in self._n_gram_trie.n_gram_frequencies.items():
            ngram = [str(i) for i in ngram]
            ngram = ''.join(ngram)
            if context in ngram[:-1]:
                total += freq
        try:
            return ngram_freq / total
        except ZeroDivisionError:
            return None

    def _generate_next_word(self, context: tuple) -> int:
        if not isinstance(context, tuple):
            raise ValueError
        if not len(context) == len(self._n_gram_trie.n_grams[0]) - 1:
            raise ValueError

        smart_frequencies = {}
        for word in self._word_storage.storage.values():
            smart_frequencies[word] = self._calculate_maximum_likelihood(word, context)
        if list(smart_frequencies.values())[0] == None:
            unis = list(self._n_gram_trie.uni_grams.items())
            unis.sort(key=lambda x: x[1], reverse=True)
            return int(unis[0][0][0])
        items = list(smart_frequencies.items())
        items.sort(key=lambda x: x[1], reverse=True)
        return items[0][0]


class BackOffGenerator(NGramTextGenerator):

    def __init__(self, word_storage: WordStorage, n_gram_trie: NGramTrie, *args):
        super().__init__(word_storage, n_gram_trie)

    def _generate_next_word(self, context: tuple) -> int:
        pass


def decode_text(storage: WordStorage, encoded_text: tuple) -> tuple:
    sentences = []
    sentence = []
    stop_word = storage.get_id('<END>')
    for word in encoded_text:
        if not word == stop_word:
            word = storage.get_word(word)
            sentence.append(word)
        else:
            sentences.append(sentence)
            sentence = []
    sentences = [' '.join([sentence[0][0].upper() + sentence[0][1:]] + sentence[1:]) for sentence in sentences]
    return sentences



def save_model(model: NGramTextGenerator, path_to_saved_model: str):
    pass


def load_model(path_to_saved_model: str) -> NGramTextGenerator:
    pass

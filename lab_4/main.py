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
    print(sentences)
    tokenized = [tokenize_by_words(sentence) for sentence in sentences]
    print(tokenized)
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
        pass

    def _generate_next_word(self, context: tuple) -> int:
        pass

    def _generate_sentence(self, context: tuple) -> tuple:
        pass

    def generate_text(self, context: tuple, number_of_sentences: int) -> tuple:
        pass


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

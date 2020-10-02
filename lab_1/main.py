"""
Lab 1
A concordance extraction
"""


def tokenize(text: str) -> list:
    if not isinstance(text, str):
        return []

    clean_tokens = []
    for token in text.lower().split():
        word = ''
        for character in token:
            if character.isalpha():
                word += character
        if word:
            clean_tokens.append(word)
    return clean_tokens


def remove_stop_words(tokens: list, stop_words: list) -> list:
"""
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    stop_words = ['the', 'is']
    --> ['weather', 'sunny', 'man', 'happy']
"""
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return []

    return [token for token in tokens if token not in stop_words]


def calculate_frequencies(tokens: list) -> dict:
    if not isinstance(tokens, list) or None in tokens:
        return {}

    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1
        else:
            freq_dict[token] = 1
    return freq_dict



def get_top_n_words(freq_dict: dict, top_n: int) -> list:
    """
    Returns the most common words
    :param freq_dict: a dictionary with frequencies
    :param top_n: a number of the most common words to return
    :return: a list of the most common words
    e.g. tokens = ['weather', 'sunny', 'man', 'happy', 'and', 'dog', 'happy']
    top_n = 1
    --> ['happy']
    """
    
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int) or None in freq_dict:
        return []

   
    frequencies_and_words_sorted = sorted(list(freq_dict.items()), key=lambda i: i[1], reverse=True)
    result = []
    for word_freq in frequencies_and_words_sorted[:top_n]:
        result.append(word_freq[0])
    return result


def get_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int) -> list:
    """
    Gets a concordance of a word
    A concordance is a listing of each occurrence of a word in a text,
    presented with the words surrounding it
    :param tokens: a list of tokens
    :param word: a word-base for a concordance
    :param left_context_size: the number of words in the left context
    :param right_context_size: the number of words in the right context
    :return: a concordance
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    --> [['man', 'is', 'happy', 'the', 'dog', 'is'], ['dog', 'is', 'happy', 'but', 'the', 'cat']]
    """
    if not isinstance(tokens, list) or not isinstance(word, str)\
            or None in tokens:
        return []
    if left_context_size is True or right_context_size is True\
            or not isinstance(left_context_size, int) or not isinstance(right_context_size, int):
        return []

    if left_context_size < 0:
        left_context_size = 0
    if right_context_size < 0:
        right_context_size = 0
    if left_context_size == 0 and right_context_size == 0:
        return []

    contexts = []
    for index, element in enumerate(tokens):
        if element == word:
            contexts.append(tokens[index-left_context_size:index+right_context_size+1])
    return contexts

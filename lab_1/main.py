"""
Lab 1
A concordance extraction
"""


def tokenize(text: str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    if not isinstance(text, str):
        return []
    symbols = "'-.,!?:%&<>*#@"
    for symbol in symbols:
        text = text.replace(symbol, "")
    text = text.split()
    wordlist = []
    for element in text:
        if element.isalpha():
            wordlist.append(element.lower())
    return wordlist


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
    if not isinstance(tokens, list):
        return []
    tokens_new = []
    for element in tokens:
        if element not in stop_words:
            tokens_new.append(element)
    return tokens_new


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    if not isinstance(tokens, list):
        return {}
    if isinstance(tokens, list) and tokens:
        for el in tokens:
            if not isinstance(el, str):
                return {}
    return {element: tokens.count(element) for element in tokens}


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
    if not isinstance(freq_dict, dict) or not isinstance(top_n, int):
        return []
    top_words = []
    counter = 0
    freq_and_word = list(freq_dict.items())
    freq_and_word.sort(key=lambda x: x[1], reverse=True)
    for element in freq_and_word:
        if counter < top_n:
            top_words.append(element[0])
            counter += 1
    return top_words


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
            or not isinstance(right_context_size, int) or not (left_context_size, int):
        return []
    concordance = []
    word_index = []
    for index, element in enumerate(tokens):
        if element == word:
            word_index += [index]
    for index in word_index:
        if left_context_size > 0 and right_context_size > 0:
            concordance.append(tokens[index - left_context_size: index + right_context_size + 1])
        elif left_context_size > 0:
            concordance.append(tokens[index-left_context_size:index+1])
        elif right_context_size > 0:
            concordance.append(tokens[index: index + right_context_size + 1])
    return concordance


def get_adjacent_words(tokens: list, word: str, left_n: int, right_n: int) -> list:
    """
    Gets adjacent words from the left and right context
    :param tokens: a list of tokens
    :param word: a word-base for the search
    :param left_n: the distance between a word and an adjacent one in the left context
    :param right_n: the distance between a word and an adjacent one in the right context
    :return: a list of adjacent words
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_n = 2
    right_n = 3
    --> [['man', 'is'], ['dog, 'cat']]
    """
    if not isinstance(tokens, list) or not isinstance(word, str) \
            or not isinstance(left_n, int) or not isinstance(right_n, int):
        return []
    concord = get_concordance(tokens, word, left_n, right_n)
    adj_words = []
    for element in concord:
        if left_n > 0 and right_n > 0:
            adj_words.append([element[0], element[-1]])
        elif left_n > 0 and not right_n > 0:
            adj_words.append([element[0]])
        elif right_n > 0 and not left_n > 0:
            adj_words.append([element[-1]])
    return adj_words

def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as fs:
        data = fs.read()

    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    with open(path_to_file, 'w', encoding='utf-8') as file:
        for element in content:
            file.write(' '.join(element) + '\n')
        file.close()



def sort_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int, left_sort: bool) -> list:
    """
    Gets a concordance of a word and sorts it by either left or right context
    :param tokens: a list of tokens
    :param word: a word-base for a concordance
    :param left_context_size: the number of words in the left context
    :param right_context_size: the number of words in the right context
    :param left_sort: if True, sort by the left context, False – by the right context
    :return: a concordance
    e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad']
    word = 'happy'
    left_context_size = 2
    right_context_size = 3
    left_sort = True
    --> [['dog', 'is', 'happy', 'but', 'the', 'cat'], ['man', 'is', 'happy', 'the', 'dog', 'is']]
    """
    if not isinstance(left_sort, bool) or not isinstance(tokens, list) or not isinstance(word, str)\
            or not isinstance(left_context_size, int) or not isinstance(right_context_size, int):
        return []
    concord = get_concordance(tokens, word, left_context_size, right_context_size)
    if left_sort and left_context_size > 0:
        return sorted(concord)
    elif not left_sort and right_context_size > 0:
        return sorted(concord, key=lambda el: el[el.index(word)+1])

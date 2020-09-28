"""
Lab 1
A concordance extraction
"""


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as fs:
        data = fs.read()

    return data


#1
def tokenize(text: str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    tokens = []
    if type(text) == str:
        text = text.lower()
        for symbol in text:
            if symbol in '''1234567890-=!@#$%^&*()_+`~[]\{}|;':",./<>?''':
                text = text.replace(symbol, '')
        text = text.split()
        tokens.extend(text)
    return tokens


tokens = tokenize('Some awesome text.')
stop_words = read_from_file('stop_words.txt')
stop_words = tokenize(stop_words)


#2
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
    tokens_clean = []
    if type(tokens) == list:
        for i in tokens:
            if i not in stop_words:
                tokens_clean.append(i)
    return tokens_clean


tokens = remove_stop_words(tokens, stop_words)


#3
def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    frequency = {}
    if type(tokens) == list:
        for i in tokens:
            if type(i) == str:
                if i in frequency:
                    frequency[i] += 1
                else:
                    frequency[i] = 1
    return frequency


freq_dict = calculate_frequencies(tokens)


#4
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
    top_n_words = []
    if type(freq_dict) == dict and type(top_n) == int:
        freq_list = list(freq_dict.items())
        freq_list.sort(key=lambda x: -x[1])
        new_freq_dict = dict(freq_list)
        for i, word in enumerate(new_freq_dict):
            top_n_words.append(word)

    return top_n_words[:top_n]


tokens = tokenize('Some awesome text.')


#5
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
    concordance = []
    left_context = []
    right_context = []
    if type(tokens) == list and type(word) == str and type(left_context_size) == int and type(right_context_size) == int:
        if left_context_size <= 0 and right_context_size > 0\
                or left_context_size > 0 and right_context_size <= 0\
                or left_context_size > 0 and right_context_size > 0:
            operative_tokens = tokens[:]
            word = word.lower()
            while word in operative_tokens:
                index = operative_tokens.index(word)

                left_index = index - left_context_size
                left_context.extend(operative_tokens[left_index:index])

                right_index = index + right_context_size + 1
                right_context.extend(operative_tokens[index:right_index])

                left_context.extend(right_context[:])
                concordance.append(left_context[:])
                left_context.clear()
                right_context.clear()

                operative_tokens.remove(word)
    return concordance


#6
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
    adjacent_words = []
    words = []
    if type(tokens) == list and type(word) == str and type(left_n) == int and type(right_n) == int:
        if left_n <= 0 and right_n > 0\
                or left_n > 0 and right_n <= 0\
                or left_n > 0 and right_n > 0:

            operative_tokens = get_concordance(tokens, word, left_n, right_n)
            for i in operative_tokens:
                word = word.lower()
                i.remove(word)
                if len(i) > 2:
                    words.append(i[0])
                    words.append(i[-1])
                    adjacent_words.append(words[:])
                    words.clear()
                else:
                    adjacent_words.append(i)

    return adjacent_words


#7
def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    if type(path_to_file) == str and type(content) == list:
        with open(path_to_file, 'w', encoding='utf-8') as fs:
            for i in content:
                fs.write(' '.join(i))
                fs.write('\n')


def left_sort_alph(x):
    word = x[0]
    return word


def right_sort_alph(x):
    index = len(x) - right_context_size
    word = x[index]
    return word


#8
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
    if type(tokens) == list and type(word) == str and type(left_context_size) == int and type(right_context_size) == int and type(left_sort) == bool:
        if left_context_size < 0 or right_context_size < 0:
            return []
        word = word.lower()
        operative_tokens = get_concordance(tokens, word, left_context_size, right_context_size)

        if left_sort:
            operative_tokens.sort(key=left_sort_alph)

        elif not left_sort:
            operative_tokens.sort(key=right_sort_alph)

        return operative_tokens
    else:
        return []

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
    tokens = ""
    text = text.lower()
    for i in text:
        if i not in ".,!?^/:;-%@#$^&*()_+=><[]{}\"\'\\":
            tokens = tokens + i
    tokens = tokens.split()
    print(tokens)
    return tokens


# tokenize("The weather is sunny, the man is happy, happy man.")


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
    for word in tokens:
        if word in stop_words:
            tokens.remove(word)
    return tokens


# remove_stop_words(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy'], ['the', 'is'])

def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    freq_dict = {}
    for key in tokens:
        if key in freq_dict:
            value = freq_dict[key]
            freq_dict = freq_dict[key] + 1
        else:
            freq_dict[key] = 1

    return freq_dict


#calculate_frequencies(['weather', 'sunny', 'man', 'happy'])

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
    common_words = []
    n = 0

    sorted_dict = dict(sorted(freq_dict.items(), key=lambda item: item[1], reverse=True))
    sorted_dict = list(sorted_dict.keys())

    if top_n > len(sorted_dict):
        top_n = len(sorted_dict)
    if top_n >= 0:
        while n != top_n:
            common_words.append(sorted_dict[n])
            n = n + 1
    else:
        common_words = []

    return common_words


#get_top_n_words({'weather': 1, 'sunny': 2, 'man': 1, 'happy': 3}, 5)


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
    list_index = [i for i, x in enumerate(tokens) if x == word]

    if type(tokens) != list or type(word) != str:
        return concordance
    else:
        if left_context_size >= 0 and right_context_size >= 0:
            for i in list_index:
                concordance.append(tokens[i - left_context_size: i + right_context_size])
        elif left_context_size > 0:
            for i in list_index:
                concordance.append(tokens[i - left_context_size: i])
        elif right_context_size > 0:
            for i in list_index:
                concordance.append(tokens[i: i + right_context_size])
        return concordance


get_concordance(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                 'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad'], 'happy', 2, 3)



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
    concordance = []

    list_index = [i for i, x in enumerate(tokens) if x == word]
    for i in list_index:
        if left_n > 0 and right_n > 0:
            concordance.append([tokens[i - left_n], tokens[i + right_n]])

    return concordance


get_adjacent_words(['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy',
                    'the', 'dog', 'is', 'happy', 'but', 'the', 'cat', 'is', 'sad'], 'happy', 2, 3)


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
    pass

"""
Lab 1
A concordance extraction
"""


def tokenize(text: str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercase tokens without punctuation
    e.g. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    if not isinstance(text, str):
        return []


    signs = ",;:%#№@$&*=+`\"\'.!?—(){}[]-><|"
    clean_text = ''
    length = len(text)
    for i in range(length):  # цикл по длине строки
        if text[i] in signs:  # если в введенной строке нашли знак препинания
            clean_text += ''
        else:
            clean_text += text[i]
    clean_text = clean_text.lower()
    return clean_text.split()


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
    if not isinstance(stop_words, list):
        return tokens

    tokens = [token for token in tokens if token not in stop_words]
    return tokens


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
    for i in range(len(tokens)):
        dictionary = {}
        if isinstance(tokens[i], str):
            for elem in tokens:
                if elem in dictionary:
                    dictionary[elem] += 1
                else:
                    dictionary[elem] = 1
        return dictionary


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

    new_list = []
    frequency = list((freq_dict.items()))
    frequency.sort(key=lambda x: x[1], reverse=True)
    number = 0
    for elem in frequency:
        if number < top_n:
            new_list.append(elem[0])
            number += 1
    return new_list


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

    if not isinstance(tokens, list) or not isinstance(word, str) or not isinstance(left_context_size, int) or \
            not isinstance(right_context_size, int):
        return []
    elif (isinstance(left_context_size, bool) and isinstance(right_context_size, bool)) or \
            (left_context_size < 1 and right_context_size < 1):
        return []
    elif left_context_size < 0 or right_context_size < 0 or tokens == [] or word == '':
        return []
    for elem in tokens:
        if isinstance(elem, str):
            for i in range(len(tokens)):
                if word == tokens[i]:
                    if i - left_context_size >= 0 and i + 1 + right_context_size <= len(tokens) - 1:
                        concordance.append(tokens[i - left_context_size:i + 1 + right_context_size])
                    elif i - left_context_size < 0:
                        concordance.append(tokens[:i + 1 + right_context_size])
                    elif i + 1 + right_context_size > len(tokens) - 1:
                        concordance.append(tokens[i - left_context_size:])
                    else:
                        concordance = []
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
    adjacent_words = []
    if not isinstance(tokens, list) or not isinstance(word, str) or not isinstance(left_n, int) or \
            not isinstance(right_n, int):
        return []
    elif (isinstance(left_n, bool) and isinstance(right_n, bool)) or (left_n < 1 and right_n < 1):
        return []
    elif left_n < 0 or right_n < 0 or tokens == [] or word == '':
        return []

    concordance = get_concordance(tokens, word, left_n, right_n)
    for element in concordance:
        for i in range(len(element)):
            if word == element[i]:
                if i - left_n >= 0 and i + right_n <= len(element) - 1:
                    # если не выходим за границы
                    adjacent_words.append([element[i - left_n], element[i + right_n]])
                elif i - left_n < 0 and i + right_n > len(element) - 1:
                    # если выходим за границы с обеих сторон
                    adjacent_words.append([element[0], element[-1]])
                elif i - left_n < 0 and i + right_n <= len(element) - 1 and right_n != 0:
                    # если выходим за границу слева, но не выходим справа
                    adjacent_words.append([element[0], element[i + right_n]])
                elif left_n == 0 and i + right_n <= len(element) - 1:
                    # если не выходим за границу справа и слева никакое слово не берём
                    adjacent_words.append([element[i + right_n]])
                elif left_n == 0 and i + right_n > len(element) - 1:
                    # если выходим за границу справа и слева ничего не берём
                    adjacent_words.append([element[-1]])
                elif i + right_n > len(element) - 1 and i - left_n > 0 and left_n != 0:
                    # если выходим за границу справа, но не выходим слева
                    adjacent_words.append([element[i - left_n], element[-1]])
                elif right_n == 0 and i - left_n >= 0:
                    # если не выходим за границу слева и справа никакое слово не берём
                    adjacent_words.append([element[i - left_n]])
                elif right_n == 0 and i - left_n < 0:
                    # если выходим за границу справа и справа никакое слово не берём
                    adjacent_words.append([element[0]])

    for i in range(len(adjacent_words)):
        if word in adjacent_words[i]:
            adjacent_words[i].remove(word)
            
    return adjacent_words


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding="utf-8") as report:
        data = report.read()
    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    new_list = ''
    with open(path_to_file, 'w') as report:
        for elem in content:
            new_list = new_list + elem + '\n'
        report.write(new_list)


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

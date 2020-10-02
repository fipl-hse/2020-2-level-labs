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
    digits = '0123456789'
    length = len(text)
    for i in range(length):
        if text[i] in digits:
            return []

    signs = ",;:%#№@$&*=+`\"\'.!?—(){}[]-><|"
    clean_text = ''
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

    else:  # если всё корректно
        #        stop_words = stop_words.split()
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
    else:
        dictionary = {}
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

    if not isinstance(tokens, list) or not isinstance(word, str) or (
            left_context_size == 0 and right_context_size == 0):
        return []

    concordance = []

    for i in range(len(tokens)):
        if word == tokens[i]:
            if i - left_context_size > 0 and i + 1 + right_context_size < len(tokens) - 1:
                concordance.append(tokens[i - left_context_size:i + 1 + right_context_size])
            elif i - left_context_size < 0:
                concordance.append(tokens[i:i + 1 + right_context_size])
            elif i + 1 + right_context_size > len(tokens) - 1:
                concordance.append(tokens[i - left_context_size:i + 1])
            else:
                return []
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
    i = 0
    k = 0
    for i in range(len(tokens)):  # проверка строки на корректность
        if 48 <= ord(' '.join(tokens)[i]) <= 57 or (128 <= ord(' '.join(tokens)[i]) <= 175 or 224 <= ord(
                ' '.join(tokens)[i]) <= 243):
            k += 1
            break
    m = 0
    for i in range(len(word)):  # проверка слова на корректность
        if 48 <= ord(word[i]) <= 57 or (128 <= ord(word[i]) <= 175 or 224 <= ord(word[i]) <= 243):
            m += 1
            break

    adjacent_words = []
    if k != 0 or m != 0 or (left_n == 0 and right_n == 0) or (
            i - left_n < 0 and i + 1 + right_n > len(tokens) - 1):  # если некорректные токены
        return []
    else:
        for i in range(len(tokens)):
            if word == tokens[i]:
                if i - left_n > 0 and i + 1 + right_n < len(tokens) - 1:  # если не выходим за границы
                    adjacent_words.append([tokens[i - left_n], tokens[i + right_n]])
                elif i - left_n < 0:
                    adjacent_words.append(tokens[i + right_n])
                elif i + 1 + right_n > len(tokens) - 1:
                    adjacent_words.append(tokens[i - left_n])
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
    with open(path_to_file, 'w') as report:
        for i in range(len(content)):
            report.write(' '.join(content[i]))
            report.write('\n')


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

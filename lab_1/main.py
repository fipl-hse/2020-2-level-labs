"""
Lab 1
A concordance extraction
"""


def tokenize(text: str) -> list:
    """
    Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of lowercased tokens without punctuation
    E.G.. text = 'The weather is sunny, the man is happy.'
    --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
    """
    new_text = ""
    text = text.lower()
    trash = set("""1234567890-=!@#$%^&*()_+,./<>?;:'"[{}]"'""")
    for c in text:
        if c not in trash:
            new_text += c
    new_text = new_text.split()
    return new_text


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

    for i in tokens:
        if i is None:
            return []

    for i in stop_words:
        if i is None:
            return tokens
        else:
            for x in stop_words:
                tokens.remove(x)

    return tokens


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """

    dict = {}
    if not isinstance(tokens, list):
        return d

    for i in tokens:
        if dict.get(i):
            dict[i] += 1
        else:
            dict[i] = 1

    return dict


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
    max_list = list(freq_dict.items())
    max_list.sort(key=lambda x: -x[1])
    result = []
    for i in range(top_n):
        result.append(max_list[i][0])
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
    concordance = []
    for i, b in enumerate(tokens):
        if b == word:
            concordance += [
                tokens[
                max(0, i - left_context_size)
                :
                min(len(tokens), i + (right_context_size + 1))
                ]
            ]
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
    if left_n + right_n + 1 > len(tokens):
        return []
    concordances = get_concordance(tokens, word, left_n, right_n)
    result = []
    for concordance in concordances:
        if len(concordance) < left_n + 1 + right_n:
            if not concordance.index(word) < left_n + 1:
                result.append([concordance[0]])
            if not concordance.index(word) == left_n + 1:
                result.append([concordance[len(concordance) - 1]])
        else:
            result.append([concordance[0], concordance[len(concordance) - 1]])
    return result


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
    with open(path_to_file, 'w', encoding='utf-8') as fs:
        for element in content:
            fs.write(' '.join(element) + '\n')


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


# #test_text = read_from_file('text.txt')
# my_freq_dict = calculate_frequencies(tokenize(test_text))
# top = get_top_n_words(my_freq_dict, 1)
# print(top)
# print(tokenize(test_text))
# print(get_concordance(tokenize(test_text), 'amet', 3, 2))
# print(get_adjacent_words(tokenize(test_text), 'ipsum', 1, 5))
#
# write_to_file('result1.txt', get_concordance(tokenize(test_text), 'ex', 3, 2))

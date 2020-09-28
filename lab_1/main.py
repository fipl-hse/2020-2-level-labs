"""
Lab 1
A concordance extraction
"""


from string import punctuation


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

    if isinstance(text, str):
        text = text.lower()
        text = text.split()
        tokens = []
        for word in text:
            for element in word:
                if element in punctuation:
                    word = word.replace(element, '')
                if word.isalpha():
                    tokens.append(word)
                    break

        return tokens


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
    if (not isinstance(tokens, list)) or (not isinstance(stop_words, list)):
        return []

    for word in tokens:
        if not isinstance(word, str):
            return []

    for word in stop_words:
        if not isinstance(word, str):
            return []

    tokens_clear = []
    for word in tokens:
        if word not in stop_words:
            tokens_clear.append(word)

    return tokens_clear


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

    for word in tokens:
        if not isinstance(word, str):
            return {}

    freq_dict = {}
    for word in tokens:
        frequency_word = tokens.count(word)
        freq_dict[word] = frequency_word

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
    if (not isinstance(freq_dict, dict)) or (not isinstance(top_n, int)) or (top_n < 0):
        return []

    values_dict = {}
    for key, value in freq_dict.items():
        if value in values_dict:
            values_dict[value].append(key)
        else:
            values_dict[value] = [key]

    sorted_dict = {}
    for key in sorted(values_dict):
        sorted_dict[key] = values_dict[key]

    sorted_dict_keys = list(sorted_dict.keys())

    sorted_dict_reverse = {}
    for key in sorted_dict_keys[::-1]:
        sorted_dict_reverse[key] = sorted_dict[key]

    sorted_list = list(sorted_dict_reverse.values())

    top = []
    for index in range(len(sorted_list)):
        top.extend(sorted_list[index])

    return top[:top_n]


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
    list_type_check = (not isinstance(tokens, list)) or (not isinstance(tokens, list))
    word_check = (not isinstance(word, str)) or ((not list_type_check) and (word not in tokens))
    int_type_check = (not isinstance(left_context_size, int) and not isinstance(right_context_size, int)) \
                     or (isinstance(left_context_size, bool) and isinstance(right_context_size, bool))

    if list_type_check or word_check or int_type_check:
        return []

    if not int_type_check:
        left_size_incorrect = (not isinstance(left_context_size, int)) or (left_context_size < 1)
        right_size_incorrect = (not isinstance(right_context_size, int)) or (right_context_size < 1)
        if left_size_incorrect and not right_size_incorrect:
            left_context_size = 0
        elif not left_size_incorrect and right_size_incorrect:
            right_context_size = 0
        elif left_size_incorrect and right_size_incorrect:
            return []

    concordance = []
    for index, element in enumerate(tokens):
        if element == word:
            max_left_words = len(tokens[:index])
            max_right_words = len(tokens[(index + 1):])

            if left_context_size <= max_left_words and right_context_size <= max_right_words:
                context = tokens[(index - left_context_size):(index + right_context_size + 1)]
            else:
                if left_context_size > max_left_words and right_context_size > max_right_words:
                    context = tokens[:(index + max_right_words + 1)]
                elif left_context_size > max_left_words and right_context_size <= max_right_words:
                    context = tokens[:(index + right_context_size + 1)]
                elif left_context_size <= max_left_words and right_context_size > max_right_words:
                    context = tokens[(index - left_context_size):(index + max_right_words + 1)]
            concordance.append(context)

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
    word_check = (not isinstance(word, str)) or ((isinstance(tokens, list)) and (word not in tokens))
    int_type_check = (not isinstance(left_n, int) and not isinstance(right_n, int)) \
                     or (isinstance(left_n, bool) and isinstance(right_n, bool))

    if not isinstance(tokens, list) or word_check or int_type_check:
        return []

    if ((not isinstance(left_n, int)) or (left_n < 1)) and ((isinstance(right_n, int)) or (right_n >= 1)):
        left_n = 0
    elif ((isinstance(left_n, int)) or (left_n >= 1)) and (not isinstance(right_n, int)) or (right_n < 1):
        right_n = 0
    elif ((not isinstance(left_n, int)) or (left_n < 1)) and ((not isinstance(right_n, int)) or (right_n < 1)):
        return []

    concordance = get_concordance(tokens, word, left_n, right_n)
    adjacent_words = []
    for context in concordance:
        n_from_context = []
        for index, element in enumerate(context):
            if element == word:
                left_n_max = len(context[:index])
                right_n_max = len(context[(index + 1):])
                if not left_n:
                    if right_n <= right_n_max:
                        n_from_context.append(context[index + right_n])
                    elif right_n > right_n_max:
                        n_from_context.append(context[index + right_n_max])
                elif not right_n:
                    if left_n <= left_n_max:
                        n_from_context.append(context[index - left_n])
                    elif left_n > left_n_max:
                        n_from_context.append(context[index - left_n_max])
                else:
                    if left_n <= left_n_max and right_n <= right_n_max:
                        n_from_context.extend([context[index - left_n], context[index + right_n]])
                    elif left_n <= left_n_max and right_n > right_n_max:
                        n_from_context.extend([context[index - left_n], context[index + right_n_max]])
                    elif left_n > left_n_max and right_n <= right_n_max:
                        n_from_context.extend([context[index - left_n_max], context[index + right_n]])

        adjacent_words.append(n_from_context)

    return adjacent_words


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as text:
        data = text.read()

    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    if (not isinstance(path_to_file, str)) and (not isinstance(content, list)):
        return []

    with open(path_to_file, 'w', encoding='utf-8') as concordance_to_file:
        for context in content:
            context = ' '.join(context)
            context += '\n'
            concordance_to_file.write(context)


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
    concordance = get_concordance(tokens, word, left_context_size, right_context_size)

    int_check = not (isinstance(left_context_size, int) and isinstance(right_context_size, int))
    bool_check = not isinstance(left_sort, bool)

    if int_check or bool_check:
        return []

    if (left_context_size < 1 and left_sort) or (right_context_size < 1 and not left_sort):
        return []

    if left_sort:
        concordance.sort()
        return concordance

    dict_right_words = {}
    for context in concordance:
        right_word_index = context.index(word) + 1
        if context[right_word_index] in dict_right_words:
            dict_right_words[context[right_word_index]].append(context)
        else:
            dict_right_words[context[right_word_index]] = []
            dict_right_words[context[right_word_index]].append(context)

    right_word_list = list(dict_right_words.keys())
    right_word_list.sort()

    sorted_concordance = []
    for word in right_word_list:
        sorted_concordance.append(dict_right_words[word])
    print(sorted_concordance)

    for index, contexts in enumerate(sorted_concordance):
        sorted_concordance[index] = contexts[0]

    return sorted_concordance

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
    if text and type(text) == str:
        text = text.lower()
        text_list = text.split()
        tokens = []
        for word in text_list:
            if word.isalpha():
                tokens += [word]
            else:
                for e in word:
                    if e in punctuation:
                        word = word.replace(e, '')
                        if word.isalpha():
                            tokens += [word]
                            break
                        else:
                            continue
        return tokens
    else:
        return []


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
    if type(stop_words) != list:
        return []
    elif type(tokens) != list:
        return []
    else:
        for word in tokens:
            if type(word) != str:
                return []
        for word in stop_words:
            if type(word) != str:
                return []

        tokens_clear = []
        for word in tokens:
            if word in stop_words:
                continue
            else:
                tokens_clear += [word]
        return tokens_clear


def calculate_frequencies(tokens: list) -> dict:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens without stop words
    :return: a dictionary with frequencies
    e.g. tokens = ['weather', 'sunny', 'man', 'happy']
    --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    if type(tokens) != list:
        return {}
    else:
        for word in tokens:
            if type(word) != str:
                return {}
        freq_dict = {}
        for word in tokens:
            frequency = tokens.count(word)
            freq_dict[word] = frequency
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
    if (type(freq_dict) == dict) and (type(top_n) == int) and (top_n > 0):
        values_dict = {}
        for k, v in freq_dict.items():
            if v in values_dict:
                values_dict[v].append(k)
            else:
                values_dict[v] = [k]

        sorted_dict = {}
        for k in sorted(values_dict):
            sorted_dict[k] = values_dict[k]

        sorted_dict_keys = list(sorted_dict.keys())

        sorted_dict_reverse = {}
        for key in sorted_dict_keys[::-1]:
            sorted_dict_reverse[key] = sorted_dict[key]

        sorted_list = list(sorted_dict_reverse.values())

        list_top = []
        for i, c in enumerate(sorted_list):
            list_top.extend(sorted_list[i])
        return list_top[:top_n]
    else:
        return []


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
    if type(tokens) != list or type(word) != str or word not in tokens:
        return []
    elif type(left_context_size) != int or type(right_context_size) != int:
        if type(left_context_size) != int and type(right_context_size) != int:
            return []
        elif type(left_context_size) != int:
            left_context_size = 0
        elif type(right_context_size) != int:
            right_context_size = 0

    if left_context_size < 0 or right_context_size < 0:
        if left_context_size <= 0 and right_context_size <= 0:
            return []
        elif left_context_size <= 0:
            left_context_size = 0
        elif right_context_size <= 0:
            right_context_size = 0

    if left_context_size == 0 and right_context_size == 0:
        return []

    word = word.lower()
    concordance = []
    for i, c in enumerate(tokens):
        if c == word:
            max_left_words = len(tokens[:i])
            max_right_words = len(tokens[(i + 1):])
            print(max_left_words, max_left_words)
            if left_context_size <= max_left_words and right_context_size <= max_right_words:
                context = tokens[(i - left_context_size):(i + right_context_size + 1)]
            else:
                if left_context_size > max_left_words and right_context_size > max_right_words:
                    context = tokens[:(i + max_right_words + 1)]
                elif left_context_size > max_left_words and right_context_size <= max_right_words:
                    context = tokens[:(i + right_context_size + 1)]
                elif left_context_size <= max_left_words and right_context_size > max_right_words:
                    context = tokens[(i - left_context_size):(i + max_right_words + 1)]
            concordance.append(context)
        else:
            continue
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
    if type(tokens) != list or type(word) != str or word not in tokens:
        return []
    elif type(left_n) != int or type(right_n) != int:
        if type(left_n) != int and type(right_n) != int:
            return []
        elif type(left_n) != int:
            left_n = 0
        elif type(right_n) != int:
            right_n = 0

    if left_n < 0 or right_n < 0:
        if left_n < 0 and right_n < 0:
            return []
        elif left_n < 0:
            left_n = 0
        elif right_n < 0:
            right_n = 0
    if left_n == 0 and right_n == 0:
        return []

    concordance = get_concordance(tokens, word, left_n, right_n)
    adjacent_words = []
    for context in concordance:
        context_n = []
        for i, wd in enumerate(context):
            if wd == word:
                left_n_max = len(context[:i])
                right_n_max = len(context[(i + 1):])
                if left_n <= left_n_max or right_n <= right_n_max:
                    if left_n <= left_n_max and right_n <= right_n_max:
                        if left_n == 0:
                            right_word = context[i + right_n]
                            context_n += [right_word]
                        elif right_n == 0:
                            left_word = context[i - left_n]
                            context_n += [left_word]
                        else:
                            left_word = context[i - left_n]
                            right_word = context[i + right_n]
                            context_n += [left_word, right_word]
                    elif left_n <= left_n_max and right_n > right_n_max:
                        if left_n == 0:
                            right_word = context[i + right_n_max]
                            context_n += [right_word]
                        else:
                            left_word = context[i - left_n]
                            right_word = context[i + right_n_max]
                            context_n += [left_word, right_word]
                    elif left_n > left_n_max and right_n <= right_n_max:
                        if right_n == 0:
                            left_word = context[i - left_n_max]
                            context_n += [left_word]
                        else:
                            left_word = context[i - left_n_max]
                            right_word = context[i + right_n]
                            context_n += [left_word, right_word]
                elif left_n > left_n_max and right_n > right_n_max:
                    left_word = context[i - left_n_max]
                    right_word = context[i + right_n_max]
                    context_n += [left_word, right_word]
            else:
                continue
        adjacent_words.append(context_n)
    return adjacent_words


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
    if type(path_to_file) == str and type(content) == list:
        with open(path_to_file, 'w', encoding='utf-8') as f:
            for context in content:
                context = ' '.join(context)
                context += '\n'
                f.write(context)
    else:
        return []


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
    if type(left_context_size) != int and type(right_context_size) != int:
        return []
    elif left_context_size < 1 and left_sort:
        return []
    elif right_context_size < 1 and not left_sort:
        return []

    if type(left_sort) == bool:
        if left_sort == True:
            concordance.sort()
            return concordance
        elif left_sort == False:
            d = {}
            for context in concordance:
                right_word_index = context.index(word) + 1
                if context[right_word_index] in d:
                    d[context[right_word_index]].append(context)
                else:
                    d[context[right_word_index]] = []
                    d[context[right_word_index]].append(context)

            right_word_list = list(d.keys())
            right_word_list.sort()

            final_list = []
            for w in right_word_list:
                final_list.append(d[w])

            concordance_list = []
            for contexts in final_list:
                for context in contexts:
                    concordance_list.append(context)
            return concordance_list
    else:
        return []
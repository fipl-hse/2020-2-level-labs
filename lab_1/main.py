"""
Lab 1
A concordance extraction
"""


def checker(con_object, type_ob):
    if isinstance(con_object, type_ob) and type_ob is list:
        length = len(con_object) > 0
        bull_value = None not in con_object and bool not in con_object

        if length and bull_value:
            return True
    elif isinstance(con_object, type_ob) and type_ob is str and len(con_object) != 0:
        return True
    elif isinstance(con_object, type_ob) and type_ob is int and str(con_object) != "True":
        return True

    return False


def tokenize(text: str) -> list:
    """
      Splits sentences into tokens, converts the tokens into lowercase, removes punctuation
      :param text: the initial text
      :return: a list of lowercased tokens without punctuation
      e.g. text = 'The weather is sunny, the man is happy.'
      --> ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
      """
    tokens = []
    if not isinstance(text, str):
        return []

    for token in text.lower().split():
        token = "".join([letter for letter in token if letter.isalpha()])
        if token != "":
            tokens.append(token)
    return tokens


def get_stop_words() -> list:
    with open("stop_words.txt") as file:
        stop_words = file.readlines()
    return stop_words


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
    if not checker(tokens, list):
        return []

    return [token for token in tokens if token not in stop_words]


def calculate_frequencies(tokens: list) -> dict:
    """
        Calculates frequencies of given tokens
        :param tokens: a list of tokens without stop words
        :return: a dictionary with frequencies
        e.g. tokens = ['weather', 'sunny', 'man', 'happy']
        --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """

    if not checker(tokens, list):
        return {}

    return {token: tokens.count(token) for token in tokens}


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
    if not isinstance(freq_dict, dict):
        return []

    freq = list(freq_dict.items())
    freq_s = sorted(freq, key=lambda num: num[1], reverse=True)
    top = [freq_s[i][0] for i in range(min(top_n, len(freq_s)))]

    return top


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
    conco_all = []
    index_word = 0

    if checker(tokens, list) and checker(word, str) \
            and checker(left_context_size, int) and checker(right_context_size, int):

        if right_context_size != 0:
            right_context_size += 1

        if "".join(tokens) != word and word in tokens:
            index_word = tokens.index(word, index_word, len(tokens))

            for word_number in range(tokens.count(word)):
                concordance_left = tokens[index_word - left_context_size: index_word]
                concordance_right = tokens[index_word + 1: index_word + right_context_size]

                if concordance_left or concordance_right:
                    conco_all.append(concordance_left + tokens[index_word].split() + concordance_right)

                if word_number != tokens.count(word) - 1:
                    index_word = tokens.index(word, index_word + 1, len(tokens))
    return conco_all


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
    conco_all = []
    index_word = 0
    good_conditions = [checker(tokens, list),
                       checker(word, str),
                       checker(left_n, int),
                       checker(right_n, int),
                       left_n >= 0,
                       right_n >= 0]

    if False not in good_conditions:

        for _ in range(tokens.count(word)):
            if not tokens.index(word):
                concordance = [tokens[right_n]]
            else:
                index_word = tokens.index(word, index_word + 1, len(tokens))

                try:
                    concordance = [tokens[index_word - left_n], tokens[index_word + right_n]]
                except IndexError:
                    left = abs(index_word - left_n) > len([tokens[:index_word]])
                    right = index_word + right_n > len(tokens)

                    if not left and right:
                        concordance = tokens[index_word + 1:]
                    elif left and not right:
                        concordance = tokens[0:index_word]

            if concordance:
                conco_all.append(concordance)
    return conco_all


def read_from_file(path_to_file: str) -> str:
    """
    Opens the file and reads its content
    :return: the initial text in string format
    """
    with open(path_to_file, 'r', encoding='utf-8') as file:
        data = file.read()

    return data


def write_to_file(path_to_file: str, content: list):
    """
    Writes the result in a file
    """
    with open(path_to_file, "w", encoding="utf-8") as file:
        file.write(" ".join(content))


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
    conco_all = []
    index_word = 0
    left_context_bool, right_context_bool = False, False
    if isinstance(left_sort, bool):
        if checker(tokens, list) and checker(word, str) \
                and checker(left_context_size, int) and checker(right_context_size, int):

            condition_to_sort = (left_context_size < 0 and left_sort is True) or \
                                (right_context_size < 0 and left_sort is False)
            if right_context_size != 0:
                right_context_size += 1

            if "".join(tokens) != word and word in tokens and not condition_to_sort:
                index_word = tokens.index(word, index_word, len(tokens))

                for word_number in range(tokens.count(word)):
                    concordance_left = tokens[index_word - left_context_size: index_word]
                    concordance_right = tokens[index_word + 1: index_word + right_context_size]

                    # показатель, возможно ли сортировка
                    if concordance_left:
                        left_context_bool = True
                    if concordance_right:
                        right_context_bool = True

                    conco_all.append(concordance_left + tokens[index_word].split() + concordance_right)
                    if word_number != tokens.count(word) - 1:
                        index_word = tokens.index(word, index_word + 1, len(tokens))
            # сортировка по левой стороне
            if left_sort and left_context_bool:
                conco_all = sorted(conco_all)
            # сортировка по правой стороне
            if not left_sort and right_context_bool:
                conco_all.sort(key=lambda concord: concord[-left_context_size])

            if left_sort and not left_context_bool:
                return []
    return conco_all

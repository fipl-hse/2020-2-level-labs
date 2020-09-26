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

    for token in text.lower().split():
        token = "".join([_ for _ in token if _.isalpha()])
        tokens.append(token)
    return tokens


def get_stop_words() -> list:
    with open("stop_words.txt") as file:
        stop_words = file.readlines()
    return stop_words


def remove_stop_words(tokens: list, stop_words: list) -> list:
    tokens_clean = []
    """
       Removes stop words
       :param tokens: a list of tokens
       :param stop_words: a list of stop words
       :return: a list of tokens without stop words
       e.g. tokens = ['the', 'weather', 'is', 'sunny', 'the', 'man', 'is', 'happy']
       stop_words = ['the', 'is']
       --> ['weather', 'sunny', 'man', 'happy']
    """
    if checker(tokens, list):
        tokens_clean = [token for token in tokens if token not in stop_words]
    return tokens_clean


def calculate_frequencies(tokens: list) -> dict:
    """
        Calculates frequencies of given tokens
        :param tokens: a list of tokens without stop words
        :return: a dictionary with frequencies
        e.g. tokens = ['weather', 'sunny', 'man', 'happy']
        --> {'weather': 1, 'sunny': 1, 'man': 1, 'happy': 1}
    """
    frequencies = {}

    if checker(tokens, list):
        frequencies = {token: tokens.count(token) for token in tokens}
    return frequencies


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
    top = []
    if isinstance(freq_dict, dict):
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
        normal_concordance = left_context_size >= 0 and right_context_size >= 0

        if "".join(tokens) != word and word in tokens and normal_concordance:
            index_word = tokens.index(word, index_word, len(tokens))

            for i in range(tokens.count(word)):
                try:
                    concordance = tokens[index_word - left_context_size: index_word] \
                                  + tokens[index_word: index_word + right_context_size + 1]
                except IndexError:
                    left = index_word - left_context_size < index_word
                    right = index_word + right_context_size < len(tokens)

                    if left and right:
                        # когда шаг влево негативный
                        concordance = tokens[index_word - left_context_size: index_word] \
                                      + tokens[index_word: right_context_size + 1]
                    elif not left and right:
                        concordance = tokens[index_word: right_context_size + 1]
                    elif left and not right:
                        concordance = tokens[index_word - left_context_size:]
                    elif not (left and right):
                        concordance = tokens[index_word:]

                if concordance:
                    conco_all.append(concordance)

                if i != tokens.count(word) - 1:
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
    if checker(tokens, list) and checker(word, str) \
            and checker(left_n, int) and checker(right_n, int) \
            and left_n >= 0 and right_n >= 0:

        for i in range(tokens.count(word)):
            if tokens.index(word) == 0:
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
    with open(path_to_file, 'r', encoding='utf-8') as fs:
        data = fs.read()

    return data


def write_to_file(path_to_file: str, content: list):
    with open(path_to_file, "w", encoding="utf-8") as fs:
        fs.write(" ".join(content))


#it's not done right now
def sort_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int, left_sort: bool) -> list:
    concordance = get_concordance(tokens, word, left_context_size, right_context_size)
    if left_sort:
        concordance = sorted(concordance)
    return concordance

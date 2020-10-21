"""
Longest common subsequence problem
"""
import tokenizer

def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """
    tokens_tpl = []
    if isinstance(text, str) and text:
        text_full = text.split('\n')
        for token in text_full:
            if len(tokenizer.tokenize(token)):
                tokens = tuple(tokenizer.tokenize(token))
                tokens_tpl.append(tokens)
        return tuple(tokens_tpl)
    else:
      return ()

def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    is_rows = not isinstance(rows, bool) and isinstance(rows, int) and rows > 0
    is_columns = not isinstance(columns, bool) and isinstance(columns, int) and columns > 0
    if not is_rows or not is_columns:
        return []

    matrix = [[0] * columns for i in range(rows)]

    return matrix

def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    
    if not isinstance(first_sentence_tokens, tuple) or not len(first_sentence_tokens) or \
            not isinstance(second_sentence_tokens, tuple) or not len(second_sentence_tokens) or \
            not isinstance(first_sentence_tokens[0], str) or not isinstance(second_sentence_tokens[0], str):
        return []

    lcs = create_zero_matrix(len(first_sentence_tokens),len(second_sentence_tokens))
    for ind_1, token_1 in enumerate(first_sentence_tokens):
        for ind_2, token_2 in enumerate(second_sentence_tokens):
            if token_1 == token_2:
                lcs[ind_1][ind_2] = lcs[ind_1 - 1][ind_2 - 1] + 1
            else:
                lcs[ind_1][ind_2] = max(lcs[ind_1 - 1][ind_2], lcs[ind_1][ind_2 - 1])


    return lcs


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    '''check_first = isinstance(first_sentence_tokens, tuple) and len(first_sentence_tokens) > 0
    check_second = isinstance(second_sentence_tokens, tuple) and len(second_sentence_tokens) > 0
    check_plagiarism = isinstance(plagiarism_threshold, float) and 0 < plagiarism_threshold < 1'''

    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or \
            not isinstance(plagiarism_threshold, float):
        return -1
    if None in first_sentence_tokens or None in second_sentence_tokens or \
            plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1

    if len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
        return 0

    lcs = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if lcs:
        lcs_length = lcs[-1][-1]
    else:
        return 0

    if lcs_length / len(second_sentence_tokens) < plagiarism_threshold:
        return 0

    return lcs_length


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    incorrect_first = not isinstance(first_sentence_tokens, tuple)\
                           or len(first_sentence_tokens) == 0 or first_sentence_tokens[0] is None

    incorrect_second = not isinstance(second_sentence_tokens, tuple)\
                             or len(second_sentence_tokens) == 0 or second_sentence_tokens[0] is None \
                            

    if incorrect_first or incorrect_second:
        return ()

    matrix_check = not lcs_matrix or not isinstance(lcs_matrix, list)\
                   or not all(isinstance(i, list) for i in lcs_matrix)\
                   or not lcs_matrix[0][0] in (0, 1)\
                   or not len(lcs_matrix) == len(first_sentence_tokens)

    if matrix_check:
        return ()

    zero_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    if lcs_matrix == zero_matrix:
        return ()

    ind_first, ind_second = len(first_sentence_tokens) - 1,  len(second_sentence_tokens) - 1
    list_of_tokens = []

    while ind_first > 0 and ind_second > 0:
        if first_sentence_tokens[ind_first] == second_sentence_tokens[ind_second]:
            list_of_tokens.append(first_sentence_tokens[ind_first])
            ind_first -= 1
            ind_second -= 1
        elif lcs_matrix[ind_first - 1][ind_second] > lcs_matrix[ind_first][ind_second - 1]:
            ind_first -= 1
        else:
            ind_second -= 1

    if first_sentence_tokens[0] == second_sentence_tokens[0]:
        list_of_tokens.append(first_sentence_tokens[0])


    return tuple(list_of_tokens[::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(lcs_length, int)\
            or not isinstance(suspicious_sentence_tokens, tuple):
        return -1
    if len(suspicious_sentence_tokens) == 0:
        return 0

    if len(suspicious_sentence_tokens) < lcs_length\
            or lcs_length < 0 or isinstance(lcs_length, bool):
        return -1

    for word in suspicious_sentence_tokens:
        if not isinstance(word, str):
            return -1

    score = lcs_length / len(suspicious_sentence_tokens)

    return score



def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple, plagiarism_threshold=0.3) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """

    if not isinstance(original_text_tokens, tuple) or\
            not all(isinstance(i, tuple) for i in original_text_tokens) or\
            not all(isinstance(i, str) for token in original_text_tokens for i in token):
        return -1

    if not isinstance(suspicious_text_tokens, tuple) or\
            not all(isinstance(i, tuple) for i in suspicious_text_tokens) or\
            not all(isinstance(i, str) for token in suspicious_text_tokens for i in token):
        return -1


    if len(suspicious_text_tokens) > len(original_text_tokens):
        original_text_tokens = list(original_text_tokens)
        while len(suspicious_text_tokens) > len(original_text_tokens):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)

    score_sum = 0

    for ind, token in enumerate(suspicious_text_tokens):
        lcs = find_lcs_length(original_text_tokens[ind], token, plagiarism_threshold)
        score = calculate_plagiarism_score(lcs, token)
        score_sum += score

    return score_sum / len(suspicious_text_tokens)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    pass


def accumulate_diff_stats(original_text_tokens: tuple, suspicious_text_tokens: tuple, plagiarism_threshold=0.3) -> dict:
    """
    Accumulates the main statistics for pairs of sentences in texts:
            lcs_length, plagiarism_score and indexes of differences
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :return: a dictionary of main statistics for each pair of sentences
    including average text plagiarism, sentence plagiarism for each sentence and lcs lengths for each sentence
    {'text_plagiarism': int,
     'sentence_plagiarism': list,
     'sentence_lcs_length': list,
     'difference_indexes': list}
    """
    pass


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    pass


def find_lcs_length_optimized(first_sentence_tokens: tuple, second_sentence_tokens: tuple,
                              plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using an optimized algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    pass


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    pass

"""
Longest common subsequence problem
"""
from tokenizer import tokenize


def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """
    token = []
    sentence = text.split('\n')
    for elem in sentence:
        tuple_token = tuple(tokenize(elem))
        if tuple_token:
            token.append(tuple_token)
    return tuple(token)


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if not isinstance(rows, int) or not isinstance(columns, int) or isinstance(rows, bool) or \
            isinstance(columns, bool) or rows <= 0 or columns <= 0:
        return []
    zero_matrix = []
    for i in range(rows):
        zero_matrix.append([0] * columns)
    return zero_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or \
            (first_sentence_tokens == ()) or (second_sentence_tokens == ()):
        return []

    for token in first_sentence_tokens:
        if not isinstance(token, str) and token != '':
            return []

    for token in second_sentence_tokens:
        if not isinstance(token, str) and token != '':
            return []

    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

    for i, token1 in enumerate(first_sentence_tokens):
        for j, token2 in enumerate(second_sentence_tokens):
            if token1 == token2 and i == j:
                lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
            else:
                lcs_matrix[i][j] = max(lcs_matrix[i][j - 1], lcs_matrix[i - 1][j])
    return lcs_matrix


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or \
            not isinstance(plagiarism_threshold, float) or isinstance(plagiarism_threshold, bool) or \
            (plagiarism_threshold < 0) or (plagiarism_threshold > 1) or isinstance(first_sentence_tokens, bool) or \
            isinstance(second_sentence_tokens, bool):
        return -1
    if first_sentence_tokens == () or second_sentence_tokens == ():
        return 0
    for token in first_sentence_tokens:
        if not isinstance(token, str):
            return -1
    for token in second_sentence_tokens:
        if not isinstance(token, str):
            return -1

    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    length = lcs_matrix[-1][-1]

    if (length / len(second_sentence_tokens)) < plagiarism_threshold:
        return 0
    return length


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or \
            not isinstance(lcs_matrix, list) or isinstance(lcs_matrix, bool) or lcs_matrix == [] or \
            first_sentence_tokens == () or second_sentence_tokens == () or isinstance(first_sentence_tokens, bool) or \
            isinstance(second_sentence_tokens, bool):
        return ()
    for elem in lcs_matrix:
        if isinstance(elem, list):
            for el in elem:
                if not isinstance(el, int):
                    return ()
        else:
            return ()
    for token in first_sentence_tokens:
        if not isinstance(token, str):
            return ()
    for token in second_sentence_tokens:
        if not isinstance(token, str):
            return ()
    if (lcs_matrix[0][0] != 1 and lcs_matrix[0][0] != 0) or len(lcs_matrix) != len(first_sentence_tokens) or \
            len(lcs_matrix[0]) != len(second_sentence_tokens):
        return ()

    lcs = []
    i = len(first_sentence_tokens) - 1
    j = len(second_sentence_tokens) - 1
    while i > 0 and j > 0:
        if first_sentence_tokens[i] == second_sentence_tokens[j]:
            lcs.append(first_sentence_tokens[i])
            i -= 1
            j -= 1
        elif lcs_matrix[i-1][j] > lcs_matrix[i][j-1]:
            i -= 1
        else:
            j -= 1
    if lcs_matrix[0][0] != 0:
        lcs.append(first_sentence_tokens[0])
    return tuple(lcs[::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(suspicious_sentence_tokens, tuple) or \
            (not isinstance(lcs_length, int) and not isinstance(lcs_length, float)) or isinstance(lcs_length, bool) or \
            None in suspicious_sentence_tokens or lcs_length > len(suspicious_sentence_tokens) > 0 or lcs_length < 0:
        return -1
    if suspicious_sentence_tokens == ():
        plagiarism = 0.0
        return plagiarism

    plagiarism = lcs_length / len(suspicious_sentence_tokens)
    return plagiarism


def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple,
                                    plagiarism_threshold) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) or \
            isinstance(original_text_tokens, bool) or isinstance(suspicious_text_tokens, bool) or \
            not isinstance(plagiarism_threshold, float) or isinstance(plagiarism_threshold, bool) or \
            (plagiarism_threshold < 0) or (plagiarism_threshold > 1) or None in suspicious_text_tokens \
            or None in original_text_tokens:
        return -1
    if isinstance(original_text_tokens, tuple) and len(original_text_tokens) > 0:
        if isinstance(original_text_tokens[0], tuple) and \
                (None in original_text_tokens[0] or '' in original_text_tokens[0]):
            return -1
    if isinstance(suspicious_text_tokens, tuple) and len(suspicious_text_tokens) > 0:
        if isinstance(suspicious_text_tokens[0], tuple) and \
                (None in suspicious_text_tokens[0] or '' in suspicious_text_tokens[0]):
            return -1
    scores = []
    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += tuple([tuple([''])]) * (len(suspicious_text_tokens) - len(original_text_tokens))
    if len(original_text_tokens) > len(suspicious_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]
    for i, token1 in enumerate(original_text_tokens):
        for j, token2 in enumerate(suspicious_text_tokens):
            if i == j:
                lcs_length = int(find_lcs_length(token1, token2, plagiarism_threshold))
                score = calculate_plagiarism_score(lcs_length, token2)
                scores.append(score)
    result = sum(scores) / len(suspicious_text_tokens)
    return result


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


def find_lcs_length_optimized(first_sentence_tokens: list, second_sentence_tokens: list) -> int:
    """
    Finds a length of the longest common subsequence using the Hirschberg's algorithm
    At the same time, if the first and last tokens coincide,
    they are immediately added to lcs and not analyzed
    :param first_sentence_tokens: a list of tokens
    :param second_sentence_tokens: a list of tokens
    :return: a length of the longest common subsequence
    """
    pass

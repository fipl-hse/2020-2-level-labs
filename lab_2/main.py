"""
Longest common subsequence problem
"""
from tokenizer import tokenize
import copy


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    checks = [
        isinstance(rows, int),
        isinstance(columns, int)
    ]
    if not all(checks):
        return []

    row = [0] * rows
    matrix = [None] * columns
    for element in range(0, columns):
        matrix[element] = copy.deepcopy(row)
    return matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    checks = [
        isinstance(first_sentence_tokens, tuple),
        isinstance(second_sentence_tokens, tuple)
    ]
    if not all(checks) or not first_sentence_tokens or not second_sentence_tokens:
        return []
    for token_1 in first_sentence_tokens:
        if not isinstance(token_1, str):
            return []
    for token_2 in second_sentence_tokens:
        if not isinstance(token_2, str):
            return []

    columns = len(first_sentence_tokens)
    rows = len(second_sentence_tokens)
    matrix = create_zero_matrix(rows, columns)  # why does test_fill_lcs_matrix_calls_required_function fail!
    for index_1, element_1 in enumerate(first_sentence_tokens):
        for index_2, element_2 in enumerate(second_sentence_tokens):
            if element_1 == element_2:
                matrix[index_1][index_2] = matrix[index_1 - 1][index_2 - 1] + 1
            else:
                matrix[index_1][index_2] = max(matrix[index_1 - 1][index_2], matrix[index_1][index_2 - 1])

    return matrix


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    checks = [
        isinstance(first_sentence_tokens, tuple),
        isinstance(second_sentence_tokens, tuple),
        isinstance(plagiarism_threshold, float)
    ]
    if not all(checks):
        return 0

    matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
# (ideal for a2)   matrix = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 2, 2, 2], [1, 1, 2, 2, 2], [1, 1, 2, 2, 3], [1, 1, 2, 2, 3], [1, 1, 2, 2, 3]]
    lcs = []
    token_1 = len(first_sentence_tokens) - 1
    token_2 = len(second_sentence_tokens) - 1
    while token_1 >= 0 and token_2 >= 0:
        if first_sentence_tokens[token_1] == second_sentence_tokens[token_2]:
            lcs.append(first_sentence_tokens[token_1])
            token_1, token_2 = token_1 - 1, token_2 - 1
        elif matrix[token_1 - 1][token_2] > matrix[token_1][token_2 - 1]:
            token_1 -= 1
        else:
            token_2 -= 1
    my_threshold = len(lcs) / len(second_sentence_tokens)
    if my_threshold < 0:
        return 0

    return matrix[-1][-1]


""" выше по формуле; ниже вариант "на глаз". пока не решила, какой лучше
    for token_1 in first_sentence_tokens:
        for token_2 in second_sentence_tokens:
            if token_1 == token_2:
                lcs.append(token_1)
                print(lcs)
                break"""

sentence_first = ('the', 'dog', 'is', 'running', 'inside')
sentence_second = ('the', 'cat', 'is', 'sleeping', 'inside', 'the', 'house')
plagiarism_threshold = 0.3
a1 = find_lcs_length(sentence_first, sentence_second, plagiarism_threshold)
a2 = find_lcs_length(sentence_second, sentence_first, plagiarism_threshold)
print(a2)


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    pass


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    pass


def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple, plagiarism_threshold=0.3) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    pass


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

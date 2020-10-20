"""
Longest common subsequence problem
"""
import re
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
    if not isinstance(text, str):
        return ()

    raw_text = text.split('\n')
    list_of_sentences = [tokenize(element) for element in raw_text if tokenize(element)]
    tuple_of_sentences = tuple(tuple(sentence) for sentence in list_of_sentences if sentence)
    return tuple_of_sentences


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if not isinstance(rows, int) or isinstance(rows, bool) or rows <= 0:
        return []
    if not isinstance(columns, int) or isinstance(columns, bool) or columns <= 0:
        return []

    zero_matrix = [[0] * columns for idx in range(rows)]
    return zero_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    first_tuple = first_sentence_tokens
    second_tuple = second_sentence_tokens

    if (not isinstance(first_tuple, tuple) or
        not isinstance(second_tuple, tuple) or
        None in first_tuple or
        None in second_tuple):
        return []

    zero_matrix = create_zero_matrix(rows = len(first_tuple), columns = len(second_tuple))
    lcs_matrix = zero_matrix

    for row, token_1 in enumerate(first_tuple):
        for column, token_2 in enumerate(second_tuple):
            if token_1 == token_2:
                lcs_matrix[row][column] = lcs_matrix[row - 1][column - 1] + 1 if (row - 1 > 0 and column - 1 > 0) else 1
            else:
                if row - 1 < 0:
                    lcs_matrix[row][column] = 0 if (column - 1 < 0) else lcs_matrix[row][column - 1]
                else:
                    lcs_matrix[row][column] = lcs_matrix[row - 1][column] if (column - 1 < 0) else (
                    max(lcs_matrix[row][column - 1], lcs_matrix[row - 1][column]))
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
    if (not isinstance(plagiarism_threshold, float) or plagiarism_threshold < 0 or plagiarism_threshold > 1 or
        not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or
        None in first_sentence_tokens or None in second_sentence_tokens):
        return -1

    if not first_sentence_tokens or not second_sentence_tokens:
        return 0

    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    lcs_length = 0 if (lcs_matrix[-1][-1] / len(second_sentence_tokens) < plagiarism_threshold) else lcs_matrix[-1][-1]
    return lcs_length


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    first_tuple = first_sentence_tokens
    second_tuple = second_sentence_tokens

    if (not isinstance(first_tuple, tuple) or
        not isinstance(second_tuple, tuple) or
        not isinstance(lcs_matrix, list) or
        not lcs_matrix or
        not first_tuple or
        not second_tuple or
        len(lcs_matrix) != len(first_tuple) or
        len(lcs_matrix[0]) != len(second_tuple) or
        not lcs_matrix[0][0] in [0, 1]):
        return ()

    lcs_list = []

    for row, token_1 in reversed(list(enumerate(first_tuple))):
        for column, token_2 in reversed(list(enumerate(second_tuple))):
            if token_1 == token_2:
                lcs_list.append(token_1)
                row, column = row - 1, column - 1
            else:
                if row - 1 > column - 1:
                    row -= 1
                else:
                    column -= 1
    return tuple(reversed(lcs_list))


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if (not isinstance(lcs_length, int) or
        isinstance(lcs_length, bool) or
        not isinstance(suspicious_sentence_tokens, tuple) or
        None in suspicious_sentence_tokens):
        return -1.0

    if (lcs_length < 0 or
        len(suspicious_sentence_tokens) > 0 and lcs_length > len(suspicious_sentence_tokens) or
        lcs_length == 0 and len(suspicious_sentence_tokens) == 0):
        return -1.0

    plagiarism_score = lcs_length / len(suspicious_sentence_tokens) if (suspicious_sentence_tokens) else 0.0
    return plagiarism_score


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
    if (not isinstance(plagiarism_threshold, float) or plagiarism_threshold < 0 or plagiarism_threshold > 1 or
        not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) or
        None in original_text_tokens or None in suspicious_text_tokens):
        return -1.0

    if original_text_tokens == suspicious_text_tokens:
        return 1.0

    if len(original_text_tokens) < len(suspicious_text_tokens):
        while len(original_text_tokens) != len(suspicious_text_tokens):
            original_text_tokens += ('',)
    else:
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]

    plagiarism_scores = []

    for idx, sentence_in_text_2 in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[idx], sentence_in_text_2, plagiarism_threshold)
        result = (calculate_plagiarism_score(lcs_length, sentence_in_text_2))
        if result != -1:
            plagiarism_scores.append(result)
        else:
            plagiarism_scores.append(0.0)

    text_plagiarism_score = sum(plagiarism_scores) / len(suspicious_text_tokens)

    return text_plagiarism_score


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

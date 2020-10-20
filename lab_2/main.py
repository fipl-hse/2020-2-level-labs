"""
Longest common subsequence problem
"""
from tokenizer import tokenize
from typing import Dict, Callable, List


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

    sentences = text.strip().splitlines()
    tokens = tuple(tuple(tokenize(x)) for x in sentences if x)
    return tokens


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """

    checks: List[Callable] = [
        lambda: isinstance(rows, int),
        lambda: isinstance(columns, int),
        lambda: not isinstance(rows, bool),
        lambda: not isinstance(columns, bool),
        lambda: rows > 0 and columns > 0
    ]

    for check in checks:
        if not check():
            return []

    matrix = [[0] * columns for _ in range(rows)]
    return matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    checks: List[Callable] = [
        lambda: isinstance(first_sentence_tokens, tuple),
        lambda: isinstance(second_sentence_tokens, tuple),
        lambda: first_sentence_tokens,
        lambda: second_sentence_tokens,
        lambda: all((isinstance(el, str) for el in x + y))
    ]

    x, y = first_sentence_tokens, second_sentence_tokens

    for check in checks:
        if not check():
            return []

    lcs = create_zero_matrix(len(x), len(y))

    for i, w1 in enumerate(x):
        for j, w2 in enumerate(y):
            if w1 == w2:
                lcs[i][j] = lcs[i - 1][j - 1] + 1
            else:
                lcs[i][j] = max(lcs[i][j - 1], lcs[i - 1][j])

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
    # Inspired by Cerberus
    checks: Dict[Callable, int] = {
        lambda: isinstance(first_sentence_tokens, tuple): -1,
        lambda: isinstance(second_sentence_tokens, tuple): -1,
        lambda: isinstance(plagiarism_threshold, float): -1,
        lambda: 0 <= plagiarism_threshold <= 1: -1,
        lambda: first_sentence_tokens: 0,
        lambda: second_sentence_tokens: 0,
    }

    for check, value in checks.items():
        if not check():
            return value

    x, y = first_sentence_tokens, second_sentence_tokens

    if len(x) > len(y):
        x, y = y, x

    lcs_matrix = fill_lcs_matrix(x, y)

    if not lcs_matrix:
        return -1

    lcs_length = lcs_matrix[-1][-1]

    return lcs_length if (not lcs_length / len(y) < plagiarism_threshold) else 0


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    checks: List[Callable] = [
        lambda: isinstance(first_sentence_tokens, tuple),
        lambda: isinstance(second_sentence_tokens, tuple),
        lambda: isinstance(lcs_matrix, list),
        lambda: len(lcs_matrix) == len(first_sentence_tokens),
        lambda: sum(sum(el) for el in lcs_matrix),
        lambda: lcs_matrix[0][0] in {0, 1}
    ]

    for check in checks:
        if not check():
            return ()

    x, y = first_sentence_tokens, second_sentence_tokens

    if len(x) > len(y):
        x, y = y, x

    i, j = len(x) - 1, len(y) - 1
    lcs = []

    while i >= 0 and j >= 0:
        if x[i] == y[j]:
            lcs.append(x[i])
            i, j = i - 1, j - 1
        elif lcs_matrix[i - 1][j] > lcs_matrix[i][j - 1]:
            i -= 1
        else:
            j -= 1

    if lcs_matrix[0][0]:
        lcs.append(x[0])

    return tuple(lcs[::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    checks: Dict[Callable, float] = {
        lambda: isinstance(lcs_length, int): -1.0,
        lambda: not isinstance(lcs_length, bool): -1.0,
        lambda: isinstance(suspicious_sentence_tokens, tuple): -1.0,
        lambda: suspicious_sentence_tokens: 0.0,
        lambda: 0 <= lcs_length <= len(suspicious_sentence_tokens): -1.0,
        lambda: all((isinstance(el, str) for el in suspicious_sentence_tokens)): -1.0,
    }

    for check, value in checks.items():
        if not check():
            return value

    return lcs_length / len(suspicious_sentence_tokens)


def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple,
                                    plagiarism_threshold=0.3) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    checks: List[Callable] = [
        lambda: isinstance(original_text_tokens, tuple),
        lambda: isinstance(suspicious_text_tokens, tuple),
        lambda: isinstance(plagiarism_threshold, float),
        lambda: 0 <= plagiarism_threshold <= 1,
        lambda: all(all(sent) for sent in original_text_tokens + suspicious_text_tokens)
    ]

    for check in checks:
        if not check():
            return -1.0

    origin = original_text_tokens
    suspicious = suspicious_text_tokens
    length_diff = len(origin) - len(suspicious)
    plagiarism_sum = []

    if length_diff < 0:
        origin += tuple('' for _ in range(abs(length_diff)))
        origin, suspicious = suspicious, origin

    for sent_1, sent_2 in zip(origin, suspicious):
        lcs_length = find_lcs_length(sent_1, sent_2, plagiarism_threshold)
        plagiarism_sum.append(abs(calculate_plagiarism_score(lcs_length, sent_2)))

    return sum(plagiarism_sum) / len(plagiarism_sum)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    checks = [
        isinstance(original_sentence_tokens, tuple),
        isinstance(suspicious_sentence_tokens, tuple),
        isinstance(lcs, tuple)
    ]

    if not all(checks):
        return ()

    origin = original_sentence_tokens
    suspicious = suspicious_sentence_tokens

    diff_1 = tuple(idx for idx, x in enumerate(origin) if x not in lcs)
    diff_2 = tuple(idx for idx, x in enumerate(suspicious) if x not in lcs)

    if diff_1 and diff_2:
        diff_report = (diff_1[0], diff_1[-1] + 1), (diff_2[0], diff_2[-1] + 1)
        return diff_report

    # FIXME


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
    checks = [
        isinstance(original_text_tokens, tuple),
        isinstance(suspicious_text_tokens, tuple),
    ]

    if not all(checks):
        return {}

    origin = original_text_tokens
    suspicious = suspicious_text_tokens

    text_plagiarism = calculate_text_plagiarism_score(origin, suspicious)
    sentence_plagiarism = []
    sentence_lcs_length = []
    difference_indexes = []

    for sent_1, sent_2 in zip(origin, suspicious):
        lcs_length = find_lcs_length(sent_1, sent_2, plagiarism_threshold)
        lcs_matrix = fill_lcs_matrix(sent_1, sent_2)
        lcs = find_lcs(sent_1, sent_2, lcs_matrix)
        plagiarism_score = calculate_plagiarism_score(lcs_length, sent_2)
        diffs = find_diff_in_sentence(origin, suspicious, lcs)

        sentence_plagiarism.append(plagiarism_score)
        sentence_lcs_length.append(lcs_length)
        difference_indexes.append(diffs)

    diff_stats = {
        'text_plagiarism': text_plagiarism,
        'sentence_plagiarism': sentence_plagiarism,
        'sentence_lcs_length': sentence_lcs_length,
        'difference_indexes': difference_indexes
    }

    return diff_stats


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    checks = [
        isinstance(original_text_tokens, tuple),
        isinstance(suspicious_text_tokens, tuple),
        isinstance(accumulated_diff_stats, dict)
    ]

    if not all(checks):
        return ''

    origin = original_text_tokens
    suspicious = suspicious_text_tokens

    # text_plagiarism = calculate_text_plagiarism_score(origin, suspicious)
    text_plagiarism = accumulated_diff_stats['text_plagiarism']

    for idx, sent_1, sent_2 in enumerate(zip(origin, suspicious)):
        # lcs_length = find_lcs_length(sent_1, sent_2, plagiarism_threshold=0.3)
        lcs_length = accumulated_diff_stats['sentence_lcs_length'][idx]
        # plagiarism_score = calculate_plagiarism_score(lcs_length, sent_2)
        plagiarism_score = accumulated_diff_stats['sentence_plagiarism'][idx]

        report_sentence = f'''
            - {sent_1}
            + {sent_2}

            lcs = {lcs_length}, plagiarism = {plagiarism_score * 100}%

            '''

        print(report_sentence)

    print(f'Text average plagiarism (words): {text_plagiarism * 100}%')


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

    checks = [
        isinstance(first_sentence_tokens, list),
        isinstance(second_sentence_tokens, list)
    ]

    if not all(checks):
        return 0


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    pass

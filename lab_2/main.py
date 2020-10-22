"""
Longest common subsequence problem
"""
from typing import Dict, Callable, List, Tuple
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

    checks: List[Callable[[], bool]] = [
        lambda: isinstance(rows, int),
        lambda: isinstance(columns, int),
        lambda: not isinstance(rows, bool),
        lambda: not isinstance(columns, bool),
        lambda: rows > 0 and columns > 0
    ]

    for check in checks:
        if not check():
            return []

    matrix: List[list] = [[0] * columns for _ in range(rows)]
    return matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    checks: List[Callable[[], bool]] = [
        lambda: isinstance(first_sentence_tokens, tuple),
        lambda: isinstance(second_sentence_tokens, tuple),
        lambda: first_sentence_tokens,
        lambda: second_sentence_tokens,
        lambda: all((isinstance(el, str) for el in first_sentence_tokens + second_sentence_tokens))
    ]

    for check in checks:
        if not check():
            return []

    s_1, s_2 = first_sentence_tokens, second_sentence_tokens

    lcs: List[list] = create_zero_matrix(len(s_1), len(s_2))

    for i, w_1 in enumerate(s_1):
        for j, w_2 in enumerate(s_2):
            if w_1 == w_2:
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
    checks: Dict[Callable[[], bool], int] = {
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

    s_1, s_2 = first_sentence_tokens, second_sentence_tokens

    if len(s_1) > len(s_2):
        s_1, s_2 = s_2, s_1

    lcs_matrix: List[list] = fill_lcs_matrix(s_1, s_2)

    if not lcs_matrix:
        return -1

    lcs_length: int = lcs_matrix[-1][-1]

    return lcs_length if (not lcs_length / len(s_2) < plagiarism_threshold) else 0


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    checks: List[Callable[[], bool]] = [
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

    s_1, s_2 = first_sentence_tokens, second_sentence_tokens

    if len(s_1) > len(s_2):
        s_1, s_2 = s_2, s_1

    i, j = len(s_1) - 1, len(s_2) - 1
    lcs = []

    while i >= 0 and j >= 0:
        if s_1[i] == s_2[j]:
            lcs.append(s_1[i])
            i, j = i - 1, j - 1
        elif lcs_matrix[i - 1][j] > lcs_matrix[i][j - 1]:
            i -= 1
        else:
            j -= 1

    if lcs_matrix[0][0]:
        lcs.append(s_1[0])

    return tuple(lcs[::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    checks: Dict[Callable[[], bool], float] = {
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
    checks: List[Callable[[], bool]] = [
        lambda: isinstance(original_text_tokens, tuple),
        lambda: isinstance(suspicious_text_tokens, tuple),
        lambda: isinstance(plagiarism_threshold, float),
        lambda: 0 <= plagiarism_threshold <= 1,
        lambda: all(all(sent) for sent in original_text_tokens + suspicious_text_tokens)
    ]

    for check in checks:
        if not check():
            return -1.0

    origin, suspicious = original_text_tokens, suspicious_text_tokens
    length_diff = len(origin) - len(suspicious)
    plagiarism_sum = []

    if length_diff < 0:
        origin += tuple(() for _ in range(abs(length_diff)))

    for sent_1, sent_2 in zip(suspicious, origin):
        lcs_length = find_lcs_length(sent_1, sent_2, plagiarism_threshold)
        plagiarism_sum.append(calculate_plagiarism_score(lcs_length, sent_2))

    return sum(plagiarism_sum) / len(plagiarism_sum)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    checks: List[Callable[[], bool]] = [
        lambda: isinstance(original_sentence_tokens, tuple),
        lambda: isinstance(suspicious_sentence_tokens, tuple),
        lambda: isinstance(lcs, tuple),
        lambda: all(original_sentence_tokens + suspicious_sentence_tokens + lcs),
    ]

    for check in checks:
        if not check():
            return ()

    comparison = original_sentence_tokens, suspicious_sentence_tokens
    diff_report = []

    for sent in comparison:
        diff = []

        for i, token in enumerate(sent):
            if token not in lcs:

                if not i or sent[i - 1] in lcs:
                    diff.append(i)
                if sent[i + 1] or i == len(sent) - 1 in lcs:
                    diff.append(i + 1)

        diff_report.append(tuple(diff))

    return tuple(diff_report)


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
    origin = original_text_tokens
    suspicious = suspicious_text_tokens

    diff_stats = {
        'text_plagiarism': calculate_text_plagiarism_score(origin, suspicious),
        'sentence_plagiarism': [],
        'sentence_lcs_length': [],
        'difference_indexes': []
    }

    for s_1, s_2 in zip(origin, suspicious):
        lcs_length: int = find_lcs_length(s_1, s_2, plagiarism_threshold)
        lcs_matrix: List[list] = fill_lcs_matrix(s_1, s_2)
        lcs: Tuple[str] = find_lcs(s_1, s_2, lcs_matrix)

        diff_stats['sentence_plagiarism'].append(calculate_plagiarism_score(lcs_length, s_2))
        diff_stats['sentence_lcs_length'].append(find_lcs_length(s_1, s_2, plagiarism_threshold))
        diff_stats['difference_indexes'].append(find_diff_in_sentence(s_1, s_2, lcs))

    return diff_stats


def lining(tokens: tuple, idx: tuple) -> str:
    """
    Highlights differences in sentences with vertical lines
    :param tokens: a tuple of tokens
    :param idx: a tuple of indices of mismatching tokens
    :return: modified sentence with highlighted differences
    """
    tokens = list(tokens)

    for diff, ndiff in zip(*[iter(idx)] * 2):
        tokens[diff:ndiff] = [f'| {" ".join(tokens[diff: ndiff])} |']

    return ' '.join(tokens)


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    origin = original_text_tokens
    suspicious = suspicious_text_tokens
    report = []

    text_plagiarism = accumulated_diff_stats['text_plagiarism']

    for idx, sent in enumerate(zip(suspicious, origin)):
        lcs_length = accumulated_diff_stats['sentence_lcs_length'][idx]
        plagiarism_score = accumulated_diff_stats['sentence_plagiarism'][idx]
        diff_idx = accumulated_diff_stats['difference_indexes'][idx]

        sent_report = (f"- {lining(sent[1], diff_idx[1])}\n",
                       f"+ {lining(sent[0], diff_idx[0])}\n\n",
                       f"lcs = {lcs_length}, plagiarism = {plagiarism_score * 100:.1f}%\n\n")

        report.append(''.join(sent_report))

    report_summary = f'Text average plagiarism (words): {text_plagiarism * 100:.1f}%'

    return ''.join([''.join(report), report_summary])


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
    checks: Dict[Callable[[], bool], int] = {
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

    s_1, s_2 = first_sentence_tokens, second_sentence_tokens
    max_len = min(len(s_1), len(s_2))

    i = [0] * max_len
    for w_1 in s_1[:max_len]:
        prev_i = i.copy()
        for j, w_2 in enumerate(s_2[:max_len]):

            if w_1 == w_2:
                i[j] = prev_i[j - 1] + 1
            else:
                i[j] = max((i[j - 1], prev_i[j]))

    lcs_length: int = i[-1]

    return lcs_length if (not lcs_length / len(s_2) < plagiarism_threshold) else 0


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    tokens = []
    idx = {}

    file = (tokenize(row) for row in open(path_to_file, encoding='utf-8'))

    num = 0
    for line in file:
        for token in line:
            if token not in idx:
                idx[token] = num
                num += 1
            tokens.append(idx[token])

    return tuple(tokens)

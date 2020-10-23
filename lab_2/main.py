"""
Longest common subsequence problem
"""
from lab_2.tokenizer import tokenize

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

    sentences_list = []
    text = text.split('\n')
    for sentence in text:
        sentence_tokenize = tokenize(sentence)
        if sentence_tokenize:
            sentences_list.append(tuple(sentence_tokenize))
    return tuple(sentences_list)


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if not isinstance(rows, int) or not isinstance(columns, int):
        return []
    if isinstance(rows, bool) or isinstance(columns, bool):
        return []
    if rows <= 0 or columns <= 0:
        return []

    zero_matrix = [[0] * columns for i in range(rows)]
    return zero_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or None in first_sentence_tokens or None in second_sentence_tokens:
        return []

    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

    for index1, element1 in enumerate(first_sentence_tokens):
        for index2, element2 in enumerate(second_sentence_tokens):
            if element1 == element2:
                lcs_matrix[index1][index2] = lcs_matrix[index1 - 1][index2 - 1] + 1
            else:
                lcs_matrix[index1][index2] = max(lcs_matrix[index1][index2 - 1], lcs_matrix[index1 - 1][index2])
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
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or not isinstance(plagiarism_threshold, float) or None in first_sentence_tokens \
            or None in second_sentence_tokens or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1

    if len(first_sentence_tokens) == 0 or not first_sentence_tokens \
            or len(second_sentence_tokens) == 0 or not second_sentence_tokens:
        return 0

    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if len(first_sentence_tokens) > len(second_sentence_tokens):
        lcs_matrix = lcs_matrix[len(second_sentence_tokens) - 1][len(second_sentence_tokens) - 1]
    else:
        lcs_matrix = lcs_matrix[-1][-1]
    if lcs_matrix / len(second_sentence_tokens) < plagiarism_threshold:
        return 0
    return lcs_matrix


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or not isinstance(lcs_matrix, list) or not first_sentence_tokens \
            or not second_sentence_tokens or not lcs_matrix or None in lcs_matrix:
        return ()

    if lcs_matrix:
        if len(lcs_matrix) == len(first_sentence_tokens) and len(lcs_matrix[0]) == len(second_sentence_tokens):
            if lcs_matrix[0][0] > 1:
                return ()
    lcs = []
    for index1, element1 in enumerate(reversed(lcs_matrix)):
        for index2, element2 in enumerate(reversed(element1)):
            if not element1 or not element2:
                return ()
            if first_sentence_tokens[index1] == second_sentence_tokens[index2]:
                lcs.append(second_sentence_tokens[index2])
    return tuple(lcs)


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(suspicious_sentence_tokens, tuple):
        return -1.0
    if not suspicious_sentence_tokens:
        return 0.0
    for word in suspicious_sentence_tokens:
        if not isinstance(word, str):
            return -1.0
    if not isinstance(lcs_length, int) or isinstance(lcs_length, bool) or lcs_length < 0:
        return -1.0
    if lcs_length > len(suspicious_sentence_tokens):
        return -1.0

    plagiarism_score = lcs_length / len(suspicious_sentence_tokens)
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
    if not isinstance(original_text_tokens, tuple) or not original_text_tokens \
            or not isinstance(suspicious_text_tokens, tuple) or not suspicious_text_tokens:
        return -1.0
    for sentence_from_original in original_text_tokens:
        if not isinstance(sentence_from_original, tuple):
            return -1.0
        for word in sentence_from_original:
            if not isinstance(word, str):
                return -1.0
    for sentence_from_suspicious in suspicious_text_tokens:
        if not isinstance(sentence_from_suspicious, tuple):
            return -1.0
        for token in sentence_from_suspicious:
            if not isinstance(token, str):
                return -1.0

    if len(suspicious_text_tokens) < len(original_text_tokens):
        original_text_tokens = (list(original_text_tokens))[:len(suspicious_text_tokens)]
        original_text_tokens = tuple(original_text_tokens)
    elif len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens = list(original_text_tokens)
        while len(original_text_tokens) < len(suspicious_text_tokens):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)

    plagiarism_sum = 0.0
    for plagiarism in range(len(suspicious_text_tokens)):
        lcs_length = find_lcs_length(original_text_tokens[plagiarism],
                                     suspicious_text_tokens[plagiarism], plagiarism_threshold)
        plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[plagiarism])
        plagiarism_sum += plagiarism_score
    return plagiarism_sum / len(suspicious_text_tokens)


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

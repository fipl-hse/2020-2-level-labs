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
    new_text = text.split('\n')
    return tuple([tuple(tokenize(sentence)) for sentence in new_text if tokenize(sentence)])


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    is_bool = isinstance(rows, bool) and isinstance(columns, bool)
    not_int = not isinstance(rows, int) and not isinstance(columns, int)

    if is_bool or not_int or rows <= 0 or columns <= 0:
        return []

    matrix = []
    for row_index in range(rows):
        matrix += [[0 * i for i in range(columns)]]
    return matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or not all(isinstance(word, str) for word in first_sentence_tokens) \
            or not all(isinstance(word, str) for word in second_sentence_tokens):
        return []

    rows = len(first_sentence_tokens)
    cols = len(second_sentence_tokens)
    mtrx = create_zero_matrix(rows, cols)

    for i in range(rows):
        for j in range(cols):
            if first_sentence_tokens[i] == second_sentence_tokens[j]:
                if i < 0 or j < 0:
                    mtrx[i][j] = 1
                else:
                    mtrx[i][j] = mtrx[i - 1][j - 1] + 1
            else:
                if i < 0 or j < 0:
                    mtrx[i][j] = 1
                else:
                    mtrx[i][j] = max(mtrx[i][j - 1], mtrx[i - 1][j])
        return mtrx
    return []


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    lcs_mtrx = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)

    if not isinstance(plagiarism_threshold, float) or lcs_mtrx == [] \
            or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1
    elif len(lcs_mtrx) / len(second_sentence_tokens) < plagiarism_threshold or len(second_sentence_tokens) == 0:
        return 0

    return lcs_mtrx[-1][-1]


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple):
        return []
    if not isinstance(lcs_matrix, list) or None in lcs_matrix or \
            (isinstance(lcs_matrix, list) and None in lcs_matrix):
        return ()
    if isinstance(lcs_matrix, list) and len(lcs_matrix) > 0:
        if isinstance(lcs_matrix[0], list) and None in lcs_matrix[0]:
            return ()

    lcs = []
    row, col = len(first_sentence_tokens) - 1, len(second_sentence_tokens) - 1

    while row >= 0 and col >= 0:
        if first_sentence_tokens[row] == second_sentence_tokens[col]:
            lcs.append(first_sentence_tokens[row])
            row -= 1
            col -= 1
        elif row > col:
            row -= 1
        else:
            col -= 1

    lcs.reverse()
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
    if not suspicious_sentence_tokens or len(suspicious_sentence_tokens) == 0:
        return 0.0
    for token_from_sentence in suspicious_sentence_tokens:
        if not isinstance(token_from_sentence, str):
            return -1.0
    if not isinstance(lcs_length, int) or isinstance(lcs_length, bool) or lcs_length < 0:
        return -1.0
    if lcs_length > len(suspicious_sentence_tokens):
        return -1.0

    plagiarism_score = lcs_length / len(suspicious_sentence_tokens)
    return plagiarism_score


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
    if (not isinstance(original_text_tokens, tuple) or
            not all(isinstance(i, tuple) for i in original_text_tokens) or
            not all(isinstance(i, str) for subtuple in original_text_tokens for i in subtuple)):
        return -1.0

    if (not isinstance(suspicious_text_tokens, tuple) or
            not all(isinstance(i, tuple) for i in suspicious_text_tokens) or
            not all(isinstance(i, str) for subtuple in suspicious_text_tokens for i in subtuple)):
        return -1.0

    if not isinstance(plagiarism_threshold, float) or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1.0

    if (isinstance(original_text_tokens, tuple) and not any(original_text_tokens) or
            isinstance(suspicious_text_tokens, tuple) and not any(suspicious_text_tokens)):
        return 0

    original_list = list(original_text_tokens)
    if len(suspicious_text_tokens) < len(original_text_tokens):
        original_list = original_list[:len(suspicious_text_tokens)]
    elif len(original_text_tokens) < len(suspicious_text_tokens):
        original_list.append(() * (len(suspicious_text_tokens) - len(original_text_tokens)))
    original_text_tokens = tuple(original_list)

    p_result_sum = 0
    for i, suspicious_sentence in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[i], suspicious_sentence, plagiarism_threshold)
        p_score = calculate_plagiarism_score(lcs_length, suspicious_sentence)
        p_result_sum += p_score

    text_plagiarism_score = p_result_sum / len(suspicious_text_tokens)
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

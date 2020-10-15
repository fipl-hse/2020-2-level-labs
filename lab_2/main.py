"""
Longest common subsequence problem
"""
import copy
import re


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

    tokens = []
    text = text.lower()
    if text[-1] == '.':
        text = text[:-1]  # a dot at the end of the text adds another empty list --> avoid this
    text = text.split('.')
    for sentence in text:
        sentence = re.sub(r'[^a-z\s]', '', sentence)
        tokens.append(tuple(sentence.split()))

    return tuple(tokens)


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
    for index in range(0, columns):
        matrix[index] = copy.deepcopy(row)
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
    for token in first_sentence_tokens:  # bad check
        if not isinstance(token, str):
            return []
    for token in second_sentence_tokens:  # bad check
        if not isinstance(token, str):
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
    if not all(checks) or plagiarism_threshold >= 1 or plagiarism_threshold <= 0:
        return -1

    for token in first_sentence_tokens:  # bad check
        if not isinstance(token, str):
            return -1
    for token in second_sentence_tokens:  # bad check
        if not isinstance(token, str):
            return -1

    if not first_sentence_tokens or not second_sentence_tokens:  # terrible decision (fill_lcs_matrix is not good)
        return 0

    matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)  # (fill_lcs_matrix is not good)
# (ideal for a2)   matrix = [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 2, 2, 2],
    # [1, 1, 2, 2, 2], [1, 1, 2, 2, 3], [1, 1, 2, 2, 3], [1, 1, 2, 2, 3]]
    my_threshold = matrix[-1][-1] / len(second_sentence_tokens)
    if my_threshold < 0:
        return 0

    return matrix[-1][-1]


"""sentence_first = ('the', 'dog', 'is', 'running', 'inside')
sentence_second = ('the', 'cat', 'is', 'sleeping', 'inside', 'the', 'house')
plagiarism_threshold = 0.3
a1 = find_lcs_length(sentence_first, sentence_second, plagiarism_threshold)
a2 = find_lcs_length(sentence_second, sentence_first, plagiarism_threshold)
"""

def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    checks = [
        isinstance(first_sentence_tokens, tuple),
        isinstance(second_sentence_tokens, tuple),
        isinstance(lcs_matrix, list)
    ]
    if not all(checks) or not first_sentence_tokens or not second_sentence_tokens or not lcs_matrix:
        return ()
    for token in first_sentence_tokens:  # bad check
        if not isinstance(token, str):
            return ()
    for token in second_sentence_tokens:  # bad check
        if not isinstance(token, str):
            return ()
    for row in lcs_matrix:  # bad check
        if not isinstance(row, list):
            return ()
        for element in row:
            if not isinstance(element, int) or element < 0:
                return ()

# add zero row and zero column:
    operative_lcs_matrix = copy.deepcopy(lcs_matrix)
    columns = 1
    for row in operative_lcs_matrix:
        columns += 1
        row.insert(0, 0)
    zero_row = [0] * columns
    operative_lcs_matrix.insert(0, zero_row)
    first_sentence_tokens, second_sentence_tokens = list(first_sentence_tokens), list(second_sentence_tokens)
    first_sentence_tokens.insert(0, '_')
    second_sentence_tokens.insert(0, '__')  # avoid matching the first element

    lcs = []
    token_1, token_2 = len(first_sentence_tokens) - 1, len(second_sentence_tokens) - 1
    while token_1 >= 0 and token_2 >= 0:
        if first_sentence_tokens[token_1] == second_sentence_tokens[token_2]:
            lcs.append(first_sentence_tokens[token_1])
            token_1, token_2 = token_1 - 1, token_2 - 1  # по диагонали, если слова с соответствующими индексами равны
        elif operative_lcs_matrix[token_1][token_2 - 1] > operative_lcs_matrix[token_1 - 1][token_2]:
            token_2 -= 1  # наверх, если значение в строке с индексом -1 больше значения в столбце с индексом -1
        else:
            token_1 -= 1  # налево в остальных случаях

    lcs.reverse()
    return tuple(lcs)


"""patches_sentence = ('the', 'cat', 'is', 'sleeping')
empty_sentence = ()
lcs_matrix = []
q1 = find_lcs(empty_sentence, patches_sentence, lcs_matrix)
q2 = find_lcs(patches_sentence, empty_sentence, lcs_matrix)
q3 = find_lcs(patches_sentence, patches_sentence, lcs_matrix)
print(q2)

first_sentence = ('the', 'cat', 'is', 'sleeping')
second_sentence = ('the', 'dog', 'is', 'sleeping')
lcs_matrix = [[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 2, 2], [1, 1, 2, 3]]
l1 = find_lcs(first_sentence, second_sentence, lcs_matrix)
l2 = find_lcs(second_sentence, first_sentence, lcs_matrix)
print(l1, l2)"""


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    checks = [
        isinstance(lcs_length, int),
        type(lcs_length) != bool,
        isinstance(suspicious_sentence_tokens, tuple)
    ]
    if not all(checks) or lcs_length < 0 or lcs_length > len(suspicious_sentence_tokens)\
            or not suspicious_sentence_tokens:
        return -1.0
    for token in suspicious_sentence_tokens:  # bad check
        if not isinstance(token, str):
            return -1.0

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
    checks = [
        isinstance(original_text_tokens, tuple),
        isinstance(suspicious_text_tokens, tuple),
        isinstance(plagiarism_threshold, float)
    ]
    if not all(checks) or not original_text_tokens or not suspicious_text_tokens \
            or plagiarism_threshold > 1 or plagiarism_threshold < 0:
        return -1.0
    for sentence in original_text_tokens:  # bad check
        if not isinstance(sentence, tuple):
            return ()
        for token in sentence:
            if not isinstance(token, str):
                return ()
    for sentence in suspicious_text_tokens:  # bad check
        if not isinstance(sentence, tuple):
            return ()
        for token in sentence:
            if not isinstance(token, str):
                return ()

    if len(original_text_tokens) < len(suspicious_text_tokens):
        add = len(suspicious_text_tokens) - len(original_text_tokens)
        original_text_tokens += '' * add
    elif len(suspicious_text_tokens) < len(original_text_tokens):
        subtract = 0 - len(original_text_tokens) - len(suspicious_text_tokens)
        original_text_tokens = tuple(list(original_text_tokens)[:subtract])

    plagiarism = []
    for or_sentence in original_text_tokens:
        for su_sentence in suspicious_text_tokens:
            plagiarism.append(calculate_plagiarism_score(len(or_sentence), su_sentence))
            print(plagiarism)
    total = 0
    for res in plagiarism:
        total += res
    print(total)
    return total / len(suspicious_text_tokens)


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
    if not all(checks) or not original_sentence_tokens or not suspicious_sentence_tokens or not lcs:
        return ()
    for token in original_sentence_tokens:  # bad check
        if not isinstance(token, str):
            return ()
    for token in suspicious_sentence_tokens:  # bad check
        if not isinstance(token, str):
            return ()

    i1 = 0
    i2 = 0

    orig_diff = []
    for index in range(len(original_sentence_tokens)):
        index_or = original_sentence_tokens.index(lcs[index])
        orig_diff.append(index_or)

        while original_sentence_tokens.index(lcs[index + 1]) - original_sentence_tokens.index(lcs[index]) == 1:
            orig_diff.append(index + 1)


    while i1 <= len(original_sentence_tokens) and i2 <= len(lcs):
        if original_sentence_tokens[i1] == lcs[i2]:
            or_diff.append(i1)
            for index in range(len(original_sentence_tokens)):
                while original_sentence_tokens[i1 + index] == lcs[i2 + index]:
                    a = original_sentence_tokens.pip
            i1 += 1

        else:
            i1, i2 = i1 + 1, i2 + 1



    return diff_words


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

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
    text = text.split("\n")
    tokenized_text = [tuple(tokenize(sent)) for sent in text]
    tokenized_text = [sent for sent in tokenized_text if sent]
    return tuple(tokenized_text)


def check_object_type(object_to_check, expected_type) -> bool:
    expectations = [False]
    if expected_type is int and isinstance(object_to_check, int):
        expectations = [object_to_check >= 0,
                        object_to_check is not True]
    elif expected_type is tuple and isinstance(object_to_check, tuple):
        first_expectations = [not(isinstance(object_to_check, bool)),
                              object_to_check is not None,
                              not("" in object_to_check and len(object_to_check) == 1)]
        if first_expectations:
            if None not in object_to_check:
                expectations = [None not in [item for subtuple in object_to_check for item in subtuple]]
            else:
                expectations = [False]
        else:
            expectations = [False]

    elif expected_type is float and isinstance(object_to_check, float):
        expectations = [object_to_check is not True,
                        0 < object_to_check <= 1]
    elif expected_type is list and isinstance(object_to_check, list):
        first_expectations = [
                        object_to_check is not True,
                        object_to_check is not None,
                        ]
        if first_expectations:
            if None not in object_to_check:
                expectations = [None not in [item for sublist in object_to_check for item in sublist]]
            else:
                expectations = [False]
    if all(expectations):
        return True
    return False


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if not check_object_type(rows, int) or not check_object_type(columns, int) or \
            rows == 0 or columns == 0:
        return []
    return [[0] * columns for _ in range(rows)]


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not check_object_type(first_sentence_tokens, tuple) or not check_object_type(second_sentence_tokens, tuple):
        return []

    rows, columns = len(first_sentence_tokens), len(second_sentence_tokens)
    matrix = create_zero_matrix(rows, columns)

    for index_first, element_first in enumerate(first_sentence_tokens):
        for index_second, element_second in enumerate(second_sentence_tokens):
            if element_first == element_second:
                matrix[index_first][index_second] = matrix[index_first - 1][index_second - 1] + 1
            elif element_second != element_first:
                matrix[index_first][index_second] = max(matrix[index_first][index_second - 1],
                                                        matrix[index_first - 1][index_second])

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
    conditions = [check_object_type(first_sentence_tokens, tuple),
                  check_object_type(second_sentence_tokens, tuple),
                  isinstance(plagiarism_threshold, float)]
    if not all(conditions) or plagiarism_threshold > 1 or plagiarism_threshold < 0:
        return -1
    elif len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
        return 0

    matrix_tokens = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)

    minimum = min(len(matrix_tokens[0]), len(matrix_tokens))
    index_row, index_column = minimum, minimum
    length = matrix_tokens[index_row - 1][index_column - 1]

    if length / len(second_sentence_tokens) < plagiarism_threshold:
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
    lcs = []
    # conditions to find the subsequence
    conditions = [check_object_type(lcs_matrix, list),
                  check_object_type(first_sentence_tokens, tuple),
                  check_object_type(second_sentence_tokens, tuple)]
    if not lcs_matrix or not all(conditions):
        return ()
    if lcs_matrix[0][0] not in (1, 0):
        return ()
    elif not len(lcs_matrix[0]) == len(second_sentence_tokens) and \
            not len(lcs_matrix) == len(first_sentence_tokens):
        return ()

    row, column = len(first_sentence_tokens) - 1, len(second_sentence_tokens) - 1
    while row >= 0:
        if column < 0: # условие на перемещение
            row -= 1

        if first_sentence_tokens[row] == second_sentence_tokens[column]:
            lcs.append(first_sentence_tokens[row])

            row -= 1
            column -= 1
        elif lcs_matrix[row - 1][column] > lcs_matrix[row][column - 1]:
            row -= 1
        else:
            if column != 0:
                column -= 1
            elif column == 0:
                row -= 1

    lcs.reverse()
    return tuple(lcs)


first_sentence = ('the', 'dog', 'is', 'running')
second_sentence = ('the', 'cat', 'is', 'sleeping')
lcs_matrix = [[1, 1, 1, 1],
              [1, 1, 1, 1],
              [1, 1, 2, 2],
              [1, 1, 2, 2]]

expected = ('the', 'is')
actual = find_lcs(first_sentence, second_sentence, lcs_matrix)

def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """

    conditions = [check_object_type(lcs_length, int),
                  check_object_type(suspicious_sentence_tokens, tuple)]
    if not all(conditions) or not len(suspicious_sentence_tokens):
        return -1
    if not lcs_length:
        return 0.0
    if not lcs_length and len(suspicious_sentence_tokens) or (not(lcs_length <= len(suspicious_sentence_tokens))):
        return -1
    return lcs_length / len(suspicious_sentence_tokens)


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

    # checking the conditions
    conditions = [check_object_type(original_text_tokens, tuple),
                  check_object_type(suspicious_text_tokens, tuple),
                  check_object_type(plagiarism_threshold, float)]

    if not all(conditions):
        return -1.0

    # preparation to count the score
    if len(original_text_tokens) < len(suspicious_text_tokens):
        changed_sent_tokens = list(original_text_tokens)
        for i in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            changed_sent_tokens.append(())
        original_text_tokens = tuple(changed_sent_tokens)
    elif len(suspicious_text_tokens) < len(original_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]

    lcs = 0
    # counting
    for l_index in range(len(original_text_tokens)):
        lcs_length = find_lcs_length(original_text_tokens[l_index], suspicious_text_tokens[l_index], plagiarism_threshold)
        score = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[l_index])
        if score > 0:
            lcs += score

    # decision about the score
    p_result = lcs / len(original_text_tokens)
    if p_result < plagiarism_threshold:
        return 0.0
    return p_result


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    conditions = [check_object_type(original_sentence_tokens, tuple),
                  check_object_type(suspicious_sentence_tokens, tuple),
                  check_object_type(lcs, tuple)]
    if not(all(conditions)):
        return ()

    def count_difference(tokens):
        differences = []
        word_index = 0
        while word_index < len(tokens):
            if tokens[word_index] not in lcs:
                if word_index + 1 == len(tokens) or tokens[word_index + 1] in lcs:
                    differences.append(word_index)
                    differences.append(word_index + 1)
                    word_index += 1
                elif tokens[word_index + 1] not in lcs:
                    first_not_match = word_index
                    second_not_match = word_index
                    while second_not_match != len(tokens) - 1 and \
                            tokens[second_not_match + 1] not in lcs:
                        second_not_match += 1
                    differences.append(first_not_match)
                    differences.append(second_not_match + 1)
                    word_index = second_not_match + 1
            else:
                word_index += 1

        return tuple(differences)

    result = (count_difference(original_sentence_tokens), count_difference(suspicious_sentence_tokens))
    return result


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
    length = len(original_text_tokens)
    sentence_lcs_length = [find_lcs_length(original_text_tokens[sent], suspicious_text_tokens[sent], plagiarism_threshold)
                           for sent in range(length)]

    sentence_plagiarism = [calculate_plagiarism_score(length, suspicious_text_tokens[sent])
                           for length, sent in zip(sentence_lcs_length, range(length))]
    matrixes = [fill_lcs_matrix(original_text_tokens[sent], suspicious_text_tokens[sent])
                for sent in range(len(original_text_tokens))]
    sentence_lcs = [find_lcs(original_text_tokens[sent], suspicious_text_tokens[sent], matrix)
                    for sent, matrix in zip(range(length), matrixes)]
    difference_indexes = [find_diff_in_sentence(original_text_tokens[sent], suspicious_text_tokens[sent], lcs_one)
                          for sent, lcs_one in zip(range(len(original_text_tokens)), sentence_lcs)]

    text_score = calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)
    return {'text_plagiarism': text_score,
            'sentence_plagiarism': sentence_plagiarism,
            'sentence_lcs_length': sentence_lcs_length,
            'difference_indexes': difference_indexes}


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    result = []
    for sent_ind in range(len(original_text_tokens)):
        # here prepare the sentence
        original, suspicious = list(original_text_tokens[sent_ind]), list(suspicious_text_tokens[sent_ind])
        differences = accumulated_diff_stats['difference_indexes']
        number = 0
        for index in differences[sent_ind][0]:
            original.insert(index + number, '|')
            suspicious.insert(index + number, '|')
            number += 1
        result.append(f"- {' '.join(original)}\n+ {' '.join(suspicious)}\n"
                      f" \n"
                      f"lcs = {accumulated_diff_stats['sentence_lcs_length'][sent_ind]}, "
                      f"plagiarism = {accumulated_diff_stats['sentence_plagiarism'][sent_ind] * 100}%"
                      f" \n")
    result.append(f"Text average plagiarism (words): {accumulated_diff_stats['text_plagiarism'] * 100}%")
    return "\n".join(result)


def find_lcs_length_optimized(first_sentence_tokens: list, second_sentence_tokens: list, plagiarism_threshold: float) -> int:
    """
       Finds a length of the longest common subsequence using an optimized algorithm
       When a length is less than the threshold, it becomes 0
       :param first_sentence_tokens: a tuple of tokens
       :param second_sentence_tokens: a tuple of tokens
       :param plagiarism_threshold: a threshold
       :return: a length of the longest common subsequence
    """
    # row that we create based on the previous
    counted_row = [0] * len(second_sentence_tokens)

    for row in range(len(first_sentence_tokens)):
        # to update new row we create a copy (previous)
        previous = counted_row.copy()
        # the same logic as in usual, but save only the row
        for column in range(len(second_sentence_tokens)):
            if first_sentence_tokens[row] == second_sentence_tokens[column]:
                counted_row[column] = previous[column - 1] + 1
            else:
                counted_row[column] = max(previous[column], counted_row[column - 1])
    length = counted_row[-1]
    if length / len(second_sentence_tokens) < plagiarism_threshold:
        return 0

    return length


def tokenize_big_file(path_to_file: str) -> tuple:
    with open(path_to_file, encoding="utf-8") as first_file, open(path_to_file, encoding="utf-8") as second_file:
        first_lines = (tokenize_by_lines(line_1) for line_1 in first_file)
        second_lines = (tokenize_by_lines(line_2) for line_2 in second_file)

        lengths = (find_lcs_length_optimized(first_line, second_line, plagiarism_threshold)
                   for first_line, second_line in zip(first_lines, second_lines))

        scores = [calculate_plagiarism_score(length, line_2) for length, line_2 in zip(lengths, second_lines)]

    return tuple(scores)


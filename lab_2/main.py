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
    # main logic
    sentence_tokens = []
    for sentence in text.lower().split('.'):
        sentence_tokens.append(tuple(tokenize(sentence)))
    if sentence_tokens[-1] == ():
        return tuple(sentence_tokens[:-1])
    return tuple(sentence_tokens)


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    # checks
    if columns is True or rows is True:
        return []
    if not isinstance(rows, int) or not isinstance(columns, int)\
            or rows <= 0 or columns <= 0:
        return []

    # main logic
    zero_matrix = []
    for _ in range(0, rows):
        zero_matrix.append([])
        for _ in range(0, columns):
            zero_matrix[-1].append(0)
    #  return [ [0] * columns for _ in range(rows)]
    return zero_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    # checks
    if not isinstance(first_sentence_tokens, tuple) or\
            not isinstance(second_sentence_tokens, tuple)\
            or None in first_sentence_tokens or None in second_sentence_tokens:
        return []

    # main logic
    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    for x_i, x_elem in enumerate(first_sentence_tokens):
        for y_i, y_elem in enumerate(second_sentence_tokens):
            if x_elem == y_elem:
                lcs_matrix[x_i][y_i] = lcs_matrix[x_i - 1][y_i - 1] + 1
            else:
                lcs_matrix[x_i][y_i] = max((lcs_matrix[x_i][y_i - 1], lcs_matrix[x_i - 1][y_i]))
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
    # checks
    if not isinstance(plagiarism_threshold, float) or\
            plagiarism_threshold <= 0 or plagiarism_threshold >= 1:
        return -1
    if not isinstance(first_sentence_tokens, tuple) or\
            not isinstance(second_sentence_tokens, tuple) or\
            None in first_sentence_tokens or None in second_sentence_tokens:
        return -1
    if not second_sentence_tokens or not first_sentence_tokens:
        return 0

    # main logic. returning lcs diff size case reversed behaviour
    if len(first_sentence_tokens) > len(second_sentence_tokens):
        # to pass pylint out-of-order check, I create to new variables:
        new_first = second_sentence_tokens
        new_second = first_sentence_tokens
        lcs_matrix = fill_lcs_matrix(new_first, new_second)
        if lcs_matrix[-1][-1]/len(first_sentence_tokens) < plagiarism_threshold:
            return 0
    else:
        lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
        if lcs_matrix[-1][-1]/len(second_sentence_tokens) < plagiarism_threshold:
            return 0
    return lcs_matrix[-1][-1]


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    # checks for sentences
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) or\
            None in first_sentence_tokens or None in second_sentence_tokens:
        return ()
    # checks for matrix
    if not lcs_matrix or not isinstance(lcs_matrix, list) or\
            None in lcs_matrix or None in lcs_matrix[0] or\
            lcs_matrix[0][0] not in (0, 1):
        return ()
    # checks for matrix shape
    if not len(lcs_matrix) == len(first_sentence_tokens) and\
            not len(lcs_matrix[0]) == len(second_sentence_tokens):
        return ()

    # main logic
    lcs_tokens = []
    row_start, column_start = len(first_sentence_tokens)-1, len(second_sentence_tokens)-1
    while row_start >= 0 and column_start >= 0:
        if first_sentence_tokens[row_start] == second_sentence_tokens[row_start]:
            lcs_tokens.append(first_sentence_tokens[row_start])
            row_start -= 1
            column_start -= 1
        elif lcs_matrix[row_start-1][column_start] > lcs_matrix[row_start][column_start-1] and row_start:
            row_start -= 1
        elif lcs_matrix[row_start-1][column_start] <= lcs_matrix[row_start][column_start-1] and column_start:
            column_start -= 1
        elif not column_start and row_start:
            row_start -= 1
        else:
            column_start -= 1
    return tuple(lcs_tokens)[::-1]


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    # checks
    if not isinstance(suspicious_sentence_tokens, tuple) or\
            None in suspicious_sentence_tokens:
        return -1
    if not suspicious_sentence_tokens:
        return 0.0
    if lcs_length is True or not isinstance(lcs_length, int):
        return -1
    if lcs_length < 0 or lcs_length > len(suspicious_sentence_tokens):
        return -1

    # main logic
    return lcs_length/len(suspicious_sentence_tokens)


def calculate_text_plagiarism_score(original_text_tokens: tuple,
                                    suspicious_text_tokens: tuple,
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
    # checks
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple):
        return -1
    if None in original_text_tokens or None in suspicious_text_tokens or\
            None in original_text_tokens[0] or None in suspicious_text_tokens[0]:
        return -1
    if plagiarism_threshold is True or not isinstance(plagiarism_threshold, float):
        return -1

    # main logic
    if len(original_text_tokens) < len(suspicious_text_tokens):
        to_update = len(suspicious_text_tokens) - len(original_text_tokens)
        original_text_tokens = list(original_text_tokens)
        for _ in range(to_update):
            original_text_tokens.append('')
        original_text_tokens = tuple(original_text_tokens)

    list_lcs_text = []
    for index, element in enumerate(suspicious_text_tokens):
        lcs = find_lcs_length(original_text_tokens[index],
                              element,
                              plagiarism_threshold)
        list_lcs_text.append(calculate_plagiarism_score(lcs, element))
    return sum(list_lcs_text)/len(suspicious_text_tokens)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    # checks
    if not isinstance(original_sentence_tokens, tuple) or\
            not isinstance(suspicious_sentence_tokens, tuple) or\
            not isinstance(lcs, tuple):
        return ()
    if None in original_sentence_tokens or\
            None in suspicious_sentence_tokens or\
            None in lcs:
        return ()

    if not original_sentence_tokens and suspicious_sentence_tokens and not lcs:
        return (), (0, len(suspicious_sentence_tokens))
    if not suspicious_sentence_tokens and original_sentence_tokens and not lcs:
        return (0, len(original_sentence_tokens)), ()

    # main logic
    indices_first = []
    indices_second = []
    for index, element in enumerate(original_sentence_tokens):
        if element not in lcs:
            if original_sentence_tokens[index-1] in lcs or index == 0:
                indices_first.append(index)
                indices_second.append(index)
            try:
                if original_sentence_tokens[index+1] in lcs:
                    indices_first.append(index+1)
                    indices_second.append(index+1)
            except IndexError:
                indices_first.append(len(original_sentence_tokens))
                indices_second.append(len(suspicious_sentence_tokens))
    return tuple(indices_first), tuple(indices_second)


def accumulate_diff_stats(original_text_tokens: tuple,
                          suspicious_text_tokens: tuple,
                          plagiarism_threshold=0.3) -> dict:
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
    # main logic
    stats = {
        'text_plagiarism': 0,
        'sentence_plagiarism': [],
        'sentence_lcs_length': [],
        'difference_indexes': []
    }

    # if original text tokens length less
    if len(original_text_tokens) < len(suspicious_text_tokens):
        to_update = len(suspicious_text_tokens) - len(original_text_tokens)
        original_text_tokens = list(original_text_tokens)
        for _ in range(to_update):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)

    for index, element in enumerate(suspicious_text_tokens):
        # find_lcs_length, calculate_plagiarism_score, find diff in sentence
        lcs = find_lcs_length(original_text_tokens[index],
                              element,
                              plagiarism_threshold)
        score = calculate_plagiarism_score(lcs, element)
        lcs_matrix = fill_lcs_matrix(original_text_tokens[index],
                                     element)
        lcs_tokens = find_lcs(original_text_tokens[index],
                              element,
                              lcs_matrix)
        diff_indexes = find_diff_in_sentence(original_text_tokens[index],
                                             element,
                                             lcs_tokens)
        stats['sentence_plagiarism'].append(score)
        stats['sentence_lcs_length'].append(lcs)
        stats['difference_indexes'].append(diff_indexes)
    stats['text_plagiarism'] = calculate_text_plagiarism_score(original_text_tokens,
                                                               suspicious_text_tokens,
                                                               plagiarism_threshold)
    return stats


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    # main logic
    # if original text tokens length less
    if len(original_text_tokens) < len(suspicious_text_tokens):
        to_update = len(suspicious_text_tokens) - len(original_text_tokens)
        original_text_tokens = list(original_text_tokens)
        for _ in range(to_update):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)

    report = """"""
    for index, element in enumerate(suspicious_text_tokens):
        report += '-'
        for index_token in range(0, len(original_text_tokens[index])):
            if index_token in accumulated_diff_stats['difference_indexes'][index][0]:
                report += ' |'
            report += ' ' + original_text_tokens[index][index_token]
        report += '\n'
        report += '+ '
        for index_token_second in range(0, len(element)):
            if index_token_second in accumulated_diff_stats['difference_indexes'][index][1]:
                report += ' |'
            report += ' ' + suspicious_text_tokens[index][index_token_second]
        report += '\r\n'
        report += 'lcs = {}, plagiarism = {}%'.format(accumulated_diff_stats['sentence_lcs_length'][index],
                                                      accumulated_diff_stats['sentence_plagiarism'][index]*100)
        report += '\r\n'
    report += 'Text average plagiarism (words): {}%'.format(accumulated_diff_stats['text_plagiarism']*100)
    return report


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

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
    if not isinstance(text, str):
        return ()

    tokens = []
    text = text.split('\n')
    for sentence in text:
        sentence = tokenize(sentence)
        if sentence:
            tokens.append(tuple(sentence))

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
        not isinstance(rows, bool),
        isinstance(columns, int),
        not isinstance(columns, bool)
    ]
    if not all(checks) or rows <= 0 or columns <= 0:
        return []

    matrix = []
    for _ in range(rows):
        matrix.append([0] * columns)

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
    for token_1, token_2 in zip(first_sentence_tokens, second_sentence_tokens):
        if not isinstance(token_1, str) and not isinstance(token_1, int) \
                or not isinstance(token_2, str) and not isinstance(token_2, int):
            return []

    matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    for index_1, element_1 in enumerate(first_sentence_tokens):
        for index_2, element_2 in enumerate(second_sentence_tokens):
            if element_1 == element_2:
                matrix[index_1][index_2] = matrix[index_1 - 1][index_2 - 1] + 1
            else:
                matrix[index_1][index_2] = max(matrix[index_1 - 1][index_2], matrix[index_1][index_2 - 1])

    return matrix


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple,
                    plagiarism_threshold: float) -> int:
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
    if not first_sentence_tokens or not second_sentence_tokens:
        return 0
    for token_1, token_2 in zip(first_sentence_tokens, second_sentence_tokens):
        if not isinstance(token_1, str) and not isinstance(token_1, int)\
                or not isinstance(token_2, str) and not isinstance(token_2, int):
            return -1

    if len(first_sentence_tokens) > len(second_sentence_tokens):
        first_sentence_tokens = tuple(first_sentence_tokens[:len(second_sentence_tokens)])

    matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if not matrix:
        return 0
    my_threshold = matrix[-1][-1] / len(second_sentence_tokens)
    if my_threshold < plagiarism_threshold:
        return 0

    return matrix[-1][-1]


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

    for token_1, token_2, row in zip(first_sentence_tokens, second_sentence_tokens, lcs_matrix):
        if not isinstance(token_1, str) and not isinstance(token_1, int) \
                or not isinstance(token_2, str) and not isinstance(token_2, int) or not isinstance(row, list):
            return ()
        for element in row:
            if not isinstance(element, int) or isinstance(element, bool) or element < 0\
                    or lcs_matrix[0][0] > lcs_matrix[-1][-1] or len(lcs_matrix) != len(first_sentence_tokens)\
                    or len(lcs_matrix[0]) != len(second_sentence_tokens):
                return ()

    lcs = []
    index_row, index_col = len(first_sentence_tokens) - 1, len(second_sentence_tokens) - 1
    while index_row >= 0 and index_col >= 0:
        if first_sentence_tokens[index_row] == second_sentence_tokens[index_col]:
            lcs.append(first_sentence_tokens[index_row])
            index_row, index_col = index_row - 1, index_col - 1
        elif lcs_matrix[index_row - 1][index_col] > lcs_matrix[index_row][index_col - 1]:
            index_row -= 1
        else:
            if index_row == 1 or index_col == 0:
                index_row -= 1
            else:
                index_col -= 1

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
    checks = [
        isinstance(lcs_length, int),
        not isinstance(lcs_length, bool),
        isinstance(suspicious_sentence_tokens, tuple)
    ]
    if not all(checks) or lcs_length < 0 or lcs_length > len(suspicious_sentence_tokens):
        return -1.0
    if suspicious_sentence_tokens:
        for token in suspicious_sentence_tokens:
            if not isinstance(token, str) and not isinstance(token, int):
                return -1.0
    else:
        return 0.0

    score = lcs_length / len(suspicious_sentence_tokens)
    return score


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
    checks = [
        isinstance(original_text_tokens, tuple),
        isinstance(suspicious_text_tokens, tuple),
        isinstance(plagiarism_threshold, float)
    ]
    if not all(checks) or plagiarism_threshold > 1 or plagiarism_threshold < 0 \
            or not original_text_tokens or not suspicious_text_tokens:
        return -1.0
    for sentence_or, sentence_su in zip(original_text_tokens, suspicious_text_tokens):
        if not isinstance(sentence_or, tuple) or not isinstance(sentence_su, tuple):
            return -1.0
        for token_or, token_su in zip(sentence_or, sentence_su):
            if not isinstance(token_or, str) and not isinstance(token_or, int)\
                    or not isinstance(token_su, str) and not isinstance(token_su, int):
                return -1.0

    if len(original_text_tokens) < len(suspicious_text_tokens):
        add = (len(suspicious_text_tokens) - len(original_text_tokens))
        while add > 0:
            original_text_tokens = list(original_text_tokens)
            original_text_tokens.append(('',))
            add -= 1
        original_text_tokens = tuple(original_text_tokens)

    total = 0.0
    for sentence_index, sentence in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[sentence_index], sentence, plagiarism_threshold)
        total += calculate_plagiarism_score(lcs_length, sentence)
    result = total / len(suspicious_text_tokens)
    if result < 0:
        return 0.0

    return result


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
    if original_sentence_tokens and suspicious_sentence_tokens and lcs:
        for token_or, token_su, token_lcs in zip(original_sentence_tokens, suspicious_sentence_tokens, lcs):
            if not isinstance(token_or, str) and not isinstance(token_or, int)\
                    or not isinstance(token_su, str) and not isinstance(token_su, int)\
                    or not isinstance(token_lcs, str) and not isinstance(token_lcs, int):
                return ()

    result = []
    orig_diff = []
    for token_index, token in enumerate(original_sentence_tokens):
        if token not in lcs:
            orig_diff.append(token_index)
            orig_diff.append(token_index + 1)
    i_orig = 1
    for element in orig_diff:
        if element == orig_diff[-1]:
            pass
        elif element == orig_diff[i_orig]:
            orig_diff.remove(element)
            orig_diff.remove(element)
        else:
            i_orig += 1
    result.append(tuple(orig_diff))

    su_diff = []
    for token_index, token in enumerate(suspicious_sentence_tokens):
        if token not in lcs:
            su_diff.append(token_index)
            su_diff.append(token_index + 1)
    i_su = 1
    for element in su_diff:
        if element == su_diff[-1]:
            pass
        elif element == su_diff[i_su]:
            su_diff.remove(element)
            su_diff.remove(element)
        else:
            i_su += 1

    result.append(tuple(su_diff))
    return tuple(result)


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
        isinstance(plagiarism_threshold, float)
    ]
    if not all(checks) or plagiarism_threshold > 1 or plagiarism_threshold < 0 \
            or not original_text_tokens or not suspicious_text_tokens:
        return {}
    for sentence_or, sentence_su in zip(original_text_tokens, suspicious_text_tokens):
        if not isinstance(sentence_or, tuple) or not isinstance(sentence_su, tuple):
            return {}
        for token_or, token_su in zip(sentence_or, sentence_su):
            if not isinstance(token_or, str) and not isinstance(token_or, int) \
                    or not isinstance(token_su, str) and not isinstance(token_su, int):
                return {}

    if len(original_text_tokens) < len(suspicious_text_tokens):
        add = (len(suspicious_text_tokens) - len(original_text_tokens))
        while add > 0:
            original_text_tokens = list(original_text_tokens)
            original_text_tokens.append(('',))
            add -= 1
        original_text_tokens = tuple(original_text_tokens)

    stats = {'text_plagiarism': calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens,
                                                                plagiarism_threshold),
             'sentence_plagiarism': list,
             'sentence_lcs_length': list,
             'difference_indexes': list}

    sentence_plagiarism = []
    sentence_lcs_length = []
    difference_indexes = []
    for sentence_index, sentence in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[sentence_index], sentence, plagiarism_threshold)
        sentence_plagiarism.append(calculate_plagiarism_score(lcs_length, sentence))
        sentence_lcs_length.append(find_lcs_length(original_text_tokens[sentence_index], sentence,
                                                   plagiarism_threshold))
        matrix = fill_lcs_matrix(original_text_tokens[sentence_index], sentence)
        lcs = find_lcs(original_text_tokens[sentence_index], sentence, matrix)
        difference_indexes.append(find_diff_in_sentence(original_text_tokens[sentence_index], sentence, lcs))

    stats['sentence_plagiarism'] = sentence_plagiarism
    stats['sentence_lcs_length'] = sentence_lcs_length
    stats['difference_indexes'] = difference_indexes
    return stats


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
    if not all(checks) or not original_text_tokens or not suspicious_text_tokens or not accumulated_diff_stats:
        return ''
    for sentence_or, sentence_su in zip(original_text_tokens, suspicious_text_tokens):
        if not isinstance(sentence_or, tuple) or not isinstance(sentence_su, tuple):
            return ''
        for token_or, token_su in zip(sentence_or, sentence_su):
            if not isinstance(token_or, str) and not isinstance(token_or, int) \
                    or not isinstance(token_su, str) and not isinstance(token_su, int):
                return ''

    if len(original_text_tokens) < len(suspicious_text_tokens):
        add = (len(suspicious_text_tokens) - len(original_text_tokens))
        while add > 0:
            original_text_tokens = list(original_text_tokens)
            original_text_tokens.append(('',))
            add -= 1
        original_text_tokens = tuple(original_text_tokens)

    report = ''
    for sentence_index, sentence in enumerate(suspicious_text_tokens):
        if accumulated_diff_stats['difference_indexes'][sentence_index] == ((), ()):
            or_sentence = ' '.join(original_text_tokens[sentence_index])
            su_sentence = ' '.join(sentence)
        else:
            or_sentence = list(original_text_tokens[sentence_index])
            counter = 1
            for diff_words_index in accumulated_diff_stats['difference_indexes'][sentence_index][0]:
                if counter % 2 != 0:
                    or_sentence.insert(diff_words_index, '|')
                    counter += 1
                else:
                    or_sentence.insert(diff_words_index + 1, '|')
                    counter += 1
            or_sentence = ' '.join(or_sentence)

            su_sentence = list(sentence)
            counter = 1
            for diff_words_index in accumulated_diff_stats['difference_indexes'][sentence_index][1]:
                if counter % 2 != 0:
                    su_sentence.insert(diff_words_index, '|')
                    counter += 1
                else:
                    su_sentence.insert(diff_words_index + 1, '|')
                    counter += 1
            su_sentence = ' '.join(su_sentence)

        report += '- {}\n+ {}\n\nlcs = {}, plagiarism = {}%\n\n'.format(
            or_sentence, su_sentence, accumulated_diff_stats['sentence_lcs_length'][sentence_index],
            accumulated_diff_stats['sentence_plagiarism'][sentence_index] * 100)
    report += 'Text average plagiarism (words): {}%\n\n'.format(accumulated_diff_stats['text_plagiarism'] * 100)

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
    checks = [
        isinstance(first_sentence_tokens, tuple),
        isinstance(second_sentence_tokens, tuple),
        isinstance(plagiarism_threshold, float)
    ]
    if not all(checks) or plagiarism_threshold >= 1 or plagiarism_threshold <= 0:
        return -1
    if not first_sentence_tokens or not second_sentence_tokens:
        return 0
    for token_1, token_2 in zip(first_sentence_tokens, second_sentence_tokens):
        if not isinstance(token_1, str) and not isinstance(token_1, int)\
                or not isinstance(token_2, str) and not isinstance(token_2, int):
            return -1

    if len(first_sentence_tokens) > len(second_sentence_tokens):
        first_sentence_tokens = tuple(first_sentence_tokens[:len(second_sentence_tokens)])

    current_row = [0] * (len(second_sentence_tokens) + 1)
    for element_1 in first_sentence_tokens:
        previous_row = current_row[:]
        for index_2, element_2 in enumerate(second_sentence_tokens):
            if element_1 == element_2:
                current_row[index_2 + 1] = previous_row[index_2] + 1
            else:
                current_row[index_2 + 1] = max(current_row[index_2], previous_row[index_2 + 1])

    if not current_row:
        return 0
    my_threshold = current_row[-1] / len(second_sentence_tokens)
    if my_threshold < plagiarism_threshold:
        return 0

    return current_row[-1]


def read_in_parts(path_to_file: str, part_size=1024) -> str:
    if not isinstance(path_to_file, str):
        return ()

    with open(path_to_file, 'r', encoding='utf-8') as file_data:
        while True:
            part_data = file_data.read(part_size)
            if not part_data:
                break
            yield part_data
    return part_data


def tok(path_to_file: str) -> tuple:
    if not isinstance(path_to_file, str):
        return ()

    for part in read_in_parts(path_to_file):
        tokenized_data = tokenize_by_lines(part)
        yield tokenized_data

    return tokenized_data


cache = {}


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    if not isinstance(path_to_file, str):
        return ()

    array = ()
    tokens_dict = {}
    for piece in tok(path_to_file):
        for _, sentence in enumerate(piece):
            array += sentence

    for token in array:
        if token not in cache:
            if cache:
                token_num = cache[list(cache.keys())[-1]] + 1
            else:
                token_num = 0
            cache[token] = token_num

    for token_index, token in enumerate(array):
        tokens_dict[token_index] = cache[token]
    result = tuple(tokens_dict.values())

    return result

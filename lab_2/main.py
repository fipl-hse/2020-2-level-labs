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
        return tuple()
    sentences = re.split('[.!?]', text)
    return tuple([tuple(tokenize(token)) for token in sentences if token.strip() != ''])


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if not isinstance(rows, int) or isinstance(rows, bool) or rows < 1:
        return []

    if not isinstance(columns, int) or isinstance(columns, bool) or columns < 1:
        return []

    return [[0] * columns for _ in range(rows)]


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or len(first_sentence_tokens) == 0 or\
            not isinstance(second_sentence_tokens, tuple) or len(second_sentence_tokens) == 0:
        return []

    if not isinstance(first_sentence_tokens[0], str) or not isinstance(second_sentence_tokens[0], str):
        return []

    matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

    last = 0
    for row_i, row_elem in enumerate(first_sentence_tokens):
        for column_i, column_elem in enumerate(second_sentence_tokens):
            if row_elem == column_elem and row_i < len(second_sentence_tokens):
                matrix[row_i][column_i] = matrix[row_i - 1][column_i - 1] + 1
                last = matrix[row_i - 1][column_i - 1] + 1
            else:
                if row_i > len(second_sentence_tokens) - 1:
                    matrix[row_i][column_i] = last
                else:
                    matrix[row_i][column_i] = max((matrix[row_i][column_i - 1], matrix[row_i - 1][column_i]))

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
    if not isinstance(plagiarism_threshold, float) or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1

    matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if isinstance(first_sentence_tokens, tuple) and len(first_sentence_tokens) == 0 or\
            isinstance(second_sentence_tokens, tuple) and len(second_sentence_tokens) == 0:
        return 0
    if len(matrix) == 0:
        return -1

    max_length = matrix[-1][-1]
    plagiarism = max_length / len(second_sentence_tokens)
    if plagiarism < plagiarism_threshold:
        return 0
    return max_length


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or len(first_sentence_tokens) == 0 or\
            not isinstance(second_sentence_tokens, tuple) or len(second_sentence_tokens) == 0:
        return tuple()

    if not isinstance(first_sentence_tokens[0], str) or not isinstance(second_sentence_tokens[0], str):
        return tuple()

    if not isinstance(lcs_matrix, list) or len(lcs_matrix) == 0 or not isinstance(lcs_matrix[0], list) or\
            not isinstance(lcs_matrix[0][0], int) or max(max(lcs_matrix)) == 0:
        return tuple()

    if lcs_matrix[0][0] < 0 or lcs_matrix[0][0] > 1:
        return tuple()

    matrix = [[0] * (len(lcs_matrix[0]) + 1)]
    for row in lcs_matrix:
        matrix.append([0] + row)
    lcs_tokens = []
    row_ind, column_ind = len(first_sentence_tokens), len(second_sentence_tokens)

    while row_ind >= 1 and column_ind >= 1:
        if first_sentence_tokens[row_ind-1] == second_sentence_tokens[column_ind-1]:
            lcs_tokens.append(first_sentence_tokens[row_ind-1])
            row_ind, column_ind = row_ind - 1, column_ind - 1
        elif matrix[row_ind - 1][column_ind] > matrix[row_ind][column_ind - 1]:
            row_ind -= 1
        else:
            column_ind -= 1
    lcs_tokens.reverse()
    return tuple(lcs_tokens)


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(lcs_length, int) or isinstance(lcs_length, bool) or\
            not isinstance(suspicious_sentence_tokens, tuple) or \
            lcs_length < 0 or not all([isinstance(word, str) for word in suspicious_sentence_tokens]):
        return -1.0

    if len(suspicious_sentence_tokens) == 0:
        return 0.0

    if lcs_length > len(suspicious_sentence_tokens):
        return -1.0

    return lcs_length / len(suspicious_sentence_tokens)


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
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) or\
            not all([isinstance(word, tuple) for word in suspicious_text_tokens]) or\
            not all([isinstance(word, tuple) for word in original_text_tokens]):
        return -1.0

    plagiarism_score = 0.0
    for index, sentence in enumerate(suspicious_text_tokens):
        if index > len(original_text_tokens)-1:
            compare = ''
        else:
            compare = original_text_tokens[index]
        lcs_length = find_lcs_length(sentence, compare, plagiarism_threshold)
        plagiarism_score += calculate_plagiarism_score(lcs_length, sentence)
    print(original_text_tokens, suspicious_text_tokens, plagiarism_score, plagiarism_score/len(suspicious_text_tokens))
    return plagiarism_score/len(suspicious_text_tokens)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    if not isinstance(original_sentence_tokens, tuple) or not isinstance(suspicious_sentence_tokens, tuple) or \
            not isinstance(lcs, tuple) or not all([isinstance(word, str) for word in lcs]):
        return tuple()

    if not all([isinstance(word, str) for word in suspicious_sentence_tokens]) or \
            not all([isinstance(word, str) for word in original_sentence_tokens]):
        return tuple()

    result = []
    for sentence in [original_sentence_tokens, suspicious_sentence_tokens]:
        indexes = []
        for ind, word in enumerate(sentence):
            if word not in lcs:
                indexes.extend([ind, ind+1])
        res_sentence = [ind for ind in indexes if indexes.count(ind) == 1]
        result.append(tuple(res_sentence))

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
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple):
        return {}

    stats_dict = {
        'text_plagiarism': 0,
        'sentence_plagiarism': [],
        'sentence_lcs_length': [],
        'difference_indexes': []
    }
    for index, sentence in enumerate(suspicious_text_tokens):
        if index > len(original_text_tokens) - 1:
            compare = ''
        else:
            compare = original_text_tokens[index]
        lcs_length = find_lcs_length(sentence, compare, plagiarism_threshold)
        stats_dict['sentence_plagiarism'].append(calculate_plagiarism_score(lcs_length, sentence))
        stats_dict['sentence_lcs_length'].append(lcs_length)
        stats_dict['difference_indexes'].append(find_diff_in_sentence(
            compare,
            sentence,
            find_lcs(sentence, compare, fill_lcs_matrix(sentence, compare))))
    stats_dict['text_plagiarism'] = sum(stats_dict['sentence_plagiarism']) / len(suspicious_text_tokens)

    return stats_dict


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) or \
            not isinstance(accumulated_diff_stats, dict):
        return ''

    output_string = ''
    for index, sentence in enumerate(suspicious_text_tokens):
        if index > len(original_text_tokens) - 1:
            compare = []
        else:
            compare = list(original_text_tokens[index])
        sentence_list = list(sentence)
        inds = accumulated_diff_stats['difference_indexes'][index]
        if len(inds) > 0:
            for ind in inds[1][::-1]:
                compare.insert(ind, '|')
            for ind in inds[0][::-1]:
                sentence_list.insert(ind, '|')

        original_string = '- '+' '.join([str(word) for word in compare])
        output_string += original_string + '\n'
        print(original_string)

        suspicious_string = '+ '+' '.join([str(word) for word in sentence_list])
        output_string += suspicious_string + '\n'
        print(suspicious_string)

        len_lcs = accumulated_diff_stats["sentence_lcs_length"][index]
        plagiarism = accumulated_diff_stats["sentence_plagiarism"][index]
        plag_lcs_string = f'lcs = {len_lcs}, plagiarism = {plagiarism * 100.0}%'
        output_string += plag_lcs_string + '\n'
        print('\n', plag_lcs_string, '\n')

    text_sum_string = f'Text average plagiarism (words): {accumulated_diff_stats["text_plagiarism"] * 100}%'
    output_string += text_sum_string + '\n'
    print(text_sum_string)

    return output_string



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

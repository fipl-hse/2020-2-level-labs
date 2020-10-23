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
    text = tokenize(text)
    new_text = []
    for index, sent in enumerate(text):
        if len(tuple(text[index].split())) != 0:
            new_text.append(tuple(sent.split()))
    return tuple(new_text)

def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if (not isinstance (rows, int) or not isinstance (columns, int)
        or isinstance (rows, bool) or isinstance (columns, bool)):
        return []
    if rows < 1 or columns < 1:
        return []
    zero_matrix = []
    counter = 0
    while counter < rows:
        row_pattern = [0] * columns
        zero_matrix.append(row_pattern)
        counter += 1
    return zero_matrix

def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance (first_sentence_tokens, tuple) or not isinstance (second_sentence_tokens, tuple)\
            or len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
        return []
    list_of_tuples = [first_sentence_tokens, second_sentence_tokens]
    for current_tuple in list_of_tuples:
        for word in current_tuple:
            if not isinstance(word, str):
                return []
    matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    row_counter = 0
    for row in matrix:
        column_counter = 0
        while column_counter < len(row):
            if row_counter == 0:
                row_limit = 0
            else:
                row_limit = 1
            if column_counter == 0:
                column_limit = 0
            else:
                column_limit = 1
            if first_sentence_tokens[row_counter] == second_sentence_tokens[column_counter]:
                matrix[row_counter][column_counter] = row_limit * column_limit * \
                matrix[row_counter - 1 * row_limit][column_counter - 1 * column_limit] + 1
            else:
                matrix[row_counter][column_counter] = \
                    (max(column_limit * matrix[row_counter][column_counter - 1 * column_limit],
                    row_limit * matrix[row_counter - 1 * row_limit][column_counter]))
            column_counter += 1
        row_counter += 1
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
    if not isinstance (first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)\
            or not isinstance(plagiarism_threshold, float):
        return -1
    list_of_tuples = [first_sentence_tokens, second_sentence_tokens]
    for current_tuple in list_of_tuples:
        for word in current_tuple:
            if not isinstance(word, str):
                return -1
    if not 0 < plagiarism_threshold <= 1:
        return -1
    matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if len(matrix) > 0:
        result = matrix[-1][-1]
    else:
        result = 0
    if len(second_sentence_tokens) == 0:
        return 0
    if result/len(second_sentence_tokens) < plagiarism_threshold:
        return 0
    return result


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)\
            or not isinstance(lcs_matrix, list)\
            or not len(first_sentence_tokens) == len(lcs_matrix) != 0\
            or lcs_matrix != fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens):
        return ()
    list_of_words = []
    current_row = len(first_sentence_tokens) - 1
    current_column = len(second_sentence_tokens) - 1
    while not (current_row == 0 and current_column == 0):
        if first_sentence_tokens[current_row] == second_sentence_tokens[current_column]:
            list_of_words.append(first_sentence_tokens[current_row])
            current_row -= 1
            current_column -= 1
        elif current_row == 0:
            current_column -= 1
        elif current_column == 0:
            current_row -= 1
        elif lcs_matrix[current_row][current_column - 1] < lcs_matrix[current_row - 1][current_column]:
            current_row -= 1
        else:
            current_column -= 1
    if first_sentence_tokens[current_row] == second_sentence_tokens[current_column]:
        list_of_words.append(first_sentence_tokens[current_row])
    list_of_words.reverse()
    return tuple(list_of_words)


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(suspicious_sentence_tokens, tuple):
        return -1
    if len(suspicious_sentence_tokens) == 0:
        return 0
    if not isinstance(lcs_length, int) or lcs_length < 0 or lcs_length > len(suspicious_sentence_tokens):
        return -1
    if isinstance (lcs_length, bool):
        return -1
    for word in suspicious_sentence_tokens:
        if not isinstance (word, str):
            return -1
    plagiarism_score = lcs_length/len(suspicious_sentence_tokens)
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
    if not isinstance (original_text_tokens, tuple) or not isinstance (suspicious_text_tokens, tuple):
        return -1
    list_of_tuples = [original_text_tokens, suspicious_text_tokens]
    for current_tuple in list_of_tuples:
        for sentence in current_tuple:
            if not isinstance(sentence, tuple):
                return -1
            for word in sentence:
                if not isinstance(word, str):
                    return -1
    if not isinstance (plagiarism_threshold, float):
        return -1
    if not 0 <= plagiarism_threshold <= 1:
        return -1
    plag_summ = 0
    original_text_tokens = list(original_text_tokens)
    while len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens.append('')
    original_text_tokens = tuple(original_text_tokens)
    for sent_1, sent_2 in zip(original_text_tokens, suspicious_text_tokens):
        lcs_length = find_lcs_length(sent_1, sent_2, plagiarism_threshold)
        plagiarism_score = calculate_plagiarism_score(lcs_length, sent_2)
        if plagiarism_score == -1:
            plagiarism_score = 0
        plag_summ += plagiarism_score
    p_result = plag_summ/len(suspicious_text_tokens)
    return p_result


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    if not isinstance(original_sentence_tokens, tuple) or not isinstance (suspicious_sentence_tokens, tuple):
        return ()
    if not isinstance (lcs, tuple):
        return ()
    list_of_tuples = [original_sentence_tokens, suspicious_sentence_tokens]
    for current_tuple in list_of_tuples:
        for word in current_tuple:
            if not isinstance(word, str):
                return ()
    for word in lcs:
        if not isinstance (word, str):
            return ()
    list_of_lists = [[], []]
    list_of_tuples = [original_sentence_tokens, suspicious_sentence_tokens]
    flag = 0
    for current_list, current_tuple in zip(list_of_lists, list_of_tuples):
        for word in current_tuple:
            if word not in lcs and not flag:
                current_list.append(current_tuple.index(word))
                flag = 1
            elif word in lcs and flag:
                current_list.append(current_tuple.index(word))
                flag = 0
            if word not in lcs and current_tuple.index(word) == len(current_tuple) - 1:
                current_list.append(len(current_tuple))
        flag = 0
    result = (tuple(list_of_lists[0]), tuple(list_of_lists[1]))
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
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple):
        return {}
    list_of_tuples = [original_text_tokens, suspicious_text_tokens]
    for current_tuple in list_of_tuples:
        for sentence in current_tuple:
            if not isinstance(sentence, tuple):
                return {}
            for word in sentence:
                if not isinstance(word, str):
                    return {}
    if not isinstance(plagiarism_threshold, float):
        return {}
    if not 0 <= plagiarism_threshold <= 1:
        return {}
    result_dict = {'text_plagiarism': 0, 'sentence_plagiarism': [],
                   'sentence_lcs_length': [], 'difference_indexes': []}
    result_dict['text_plagiarism'] = calculate_text_plagiarism_score(original_text_tokens,
                                                                     suspicious_text_tokens, plagiarism_threshold)
    for sent_1, sent_2 in zip(original_text_tokens, suspicious_text_tokens):
        lcs_length = find_lcs_length(sent_1, sent_2, plagiarism_threshold)
        result_dict['sentence_lcs_length'].append(lcs_length)
        plagiarism_score = calculate_plagiarism_score(lcs_length, sent_2)
        lcs_matrix = fill_lcs_matrix(sent_1, sent_2)
        lcs = find_lcs(sent_1, sent_2, lcs_matrix)
        sent_diff = find_diff_in_sentence(sent_1, sent_2, lcs)
        if plagiarism_score == -1:
            plagiarism_score = 0
        result_dict['sentence_plagiarism'].append(plagiarism_score)
        result_dict['difference_indexes'].append(sent_diff)
    return result_dict


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple):
        return ''
    list_of_tuples = [original_text_tokens, suspicious_text_tokens]
    for current_tuple in list_of_tuples:
        for sent_1 in current_tuple:
            if not isinstance(sent_1, tuple):
                return ''
            for word in sent_1:
                if not isinstance(word, str):
                    return ''
    list_of_lists = [[], []]
    result = []
    for current_list, current_tuple in zip(list_of_lists, list_of_tuples):
        for sent_1, subtuple in zip(current_tuple, accumulated_diff_stats.get('difference_indexes')):
            sent_1 = list(sent_1)
            i = 0
            for index in subtuple[0]:
                if len(subtuple[0]) != 0:
                    sent_1.insert(index + i, '|')
                    i += 1
            sent_1 = ' '.join(sent_1)
            current_list.append(sent_1)
    for sent_1, sent_2 in zip(list_of_lists[0], list_of_lists[1]):
        current_result = ('-', sent_1, '\n' + '+', sent_2, '\n\n' + 'lcs =',
            str(accumulated_diff_stats.get('sentence_lcs_length')[list_of_lists[0].index(sent_1)]) + ',',
        'plagiarism =', str(accumulated_diff_stats.get('sentence_plagiarism')[list_of_lists[0].index(sent_1)] * 100)
        + '%', '\n\n')
        current_result = ' '.join(current_result)
        result.append(current_result)
    current_result = ('Text average plagiarism (words):', str(accumulated_diff_stats.get('text_plagiarism') * 100)
                      + '%', '\n')
    current_result = ' '.join(current_result)
    result.append(current_result)
    result = ''.join(result)
    return result


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
    return []


def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    return []

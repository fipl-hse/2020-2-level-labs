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
    tokens = []
    text = text.split('\n')
    for line in text:
        token_line = tuple(tokenize(line))
        if token_line:
            tokens.append(token_line)
    tokens = tuple(tokens)
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
    matrix = []
    if not isinstance(rows, int) or not isinstance(columns, int):
        return []
    if type(rows) == bool or type(columns) == bool:
        return []
    if columns < 1 or rows < 1:
        return []
    for i in range(rows):
        new = []
        for y in range(columns):
            new.append(0)
        matrix.append(new)
    return matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple):
        return []
    try:
        if first_sentence_tokens[0] is None or second_sentence_tokens[0] is None:
            return []
    except IndexError:
        return []
    if type(first_sentence_tokens) == bool or type(second_sentence_tokens) == bool:
        return []
    matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    for i in range(len(first_sentence_tokens)):
        line = first_sentence_tokens[:i + 1]
        length = 0
        for p, token in enumerate(second_sentence_tokens):
            if not line:
                matrix[i][p] = length
            for z, first_token in enumerate(line):
                if first_token == token:
                    length += 1
                    line = line[z + 1:]
                    matrix[i][p] = length
                    break
            matrix[i][p] = length
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
    if first_sentence_tokens == () or second_sentence_tokens == ():
        return 0
    matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if not matrix or type(plagiarism_threshold) != float:
        return -1
    if plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1
    max_len = matrix[-1][-1]
    if max_len < plagiarism_threshold:
        return 0
    else:
        return max_len


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    lcs = []
    if type(first_sentence_tokens) != tuple or type(second_sentence_tokens) != tuple:
        return lcs
    if len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
        return ()
    if first_sentence_tokens[0] is None or second_sentence_tokens[0] is None:
        return lcs
    if not lcs_matrix:
        return ()
    if type(lcs_matrix) != list:
        return ()
    if type(lcs_matrix[0]) != list:
        return ()
    if lcs_matrix[0][0] != 1 and lcs_matrix[0][0] != 0:
        return ()
    if len(lcs_matrix) != len(first_sentence_tokens) and len(lcs_matrix[0]) != len(second_sentence_tokens):
        return ()

    y = len(first_sentence_tokens) - 1  # rows
    x = len(second_sentence_tokens) - 1  # columns
    while True:
        if x == -1 or y == -1:
            break
        if first_sentence_tokens[y] == second_sentence_tokens[x]:
            lcs.append(first_sentence_tokens[y])
            x -= 1
            y -= 1
            continue
        if x == 0:
            y -= 1
            continue
        elif y == 0:
            x -= 1
            continue
        if lcs_matrix[y - 1][x] > lcs_matrix[y][x - 1]:
            y -= 1
        else:
            x -= 1
    lcs = tuple(lcs[::-1])
    return lcs

def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if type(lcs_length) != int or type(suspicious_sentence_tokens) != tuple:
        return -1
    if lcs_length < 0:
        return -1
    if len(suspicious_sentence_tokens) == 0:
        return 0
    if lcs_length > len(suspicious_sentence_tokens):
        return -1
    for token in suspicious_sentence_tokens:
        if type(token) != str or token == '':
            return -1
    result = lcs_length / len(suspicious_sentence_tokens)
    return result


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
    if type(plagiarism_threshold) != float:
        return -1
    if 0 > plagiarism_threshold or 1 < plagiarism_threshold:
        return -1
    if type(original_text_tokens) != tuple or type(suspicious_text_tokens) != tuple:
        return -1
    if len(original_text_tokens) == 0 or len(suspicious_text_tokens) == 0:
        return -1
    if type(original_text_tokens[0]) != tuple or type(suspicious_text_tokens[0]) != tuple:
        return -1
    if original_text_tokens.count(()) == len(original_text_tokens)\
            or suspicious_text_tokens.count(()) == len(suspicious_text_tokens):
        return 0
    for sentence in original_text_tokens:
        if type(sentence) == tuple and sentence:
            if None not in sentence and '' not in sentence:
                break
    else:
        return -1
    for sentence in suspicious_text_tokens:
        if type(sentence) == tuple and sentence:
            if None not in sentence and '' not in sentence:
                break
    else:
        return -1
    sus_len = len(suspicious_text_tokens)
    diff = len(original_text_tokens) - len(suspicious_text_tokens)
    p_results = []
    if diff:
        if diff > 0:
            suspicious_text_tokens = list(suspicious_text_tokens)
            for i in range(diff):
                suspicious_text_tokens.append(())
            suspicious_text_tokens = tuple(suspicious_text_tokens)
        else:
            diff *= -1
            original_text_tokens = list(original_text_tokens)
            for i in range(diff):
                original_text_tokens.append(())
            original_text_tokens = tuple(original_text_tokens)
    for i in range(len(original_text_tokens)):
        lsc = find_lcs_length(original_text_tokens[i], suspicious_text_tokens[i], plagiarism_threshold)
        p_results.append(calculate_plagiarism_score(lsc, original_text_tokens[i]))
    p_result = 0
    for i in p_results:
        if i == -1:
            continue
        p_result += i
    p_result /= sus_len
    if p_result < plagiarism_threshold:
        p_result = 0
    return p_result


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    if original_sentence_tokens != ():
        if type(original_sentence_tokens) != tuple \
                or type(suspicious_sentence_tokens) != tuple \
                or type(lcs) != tuple:
            return ()
        if original_sentence_tokens[0] is None \
                or suspicious_sentence_tokens[0]is None:
            return ()
        if lcs == (None, ):
            return ()
    first_dif = []
    second_dif = []
    lcs_copy = lcs
    for num, token in enumerate(original_sentence_tokens):
        if len(lcs_copy) == 0:
            first_dif.append(num)
            first_dif.append(len(original_sentence_tokens))
            break
        if token != lcs_copy[0]:
            first_dif.append(num)
            first_dif.append(num + 1)
        else:
            lcs_copy = lcs_copy[1:]
    for num, token in enumerate(suspicious_sentence_tokens):
        if len(lcs) == 0:
            second_dif.append(num)
            second_dif.append(len(original_sentence_tokens))
            break
        if token != lcs[0]:
            second_dif.append(num)
            second_dif.append(num + 1)
        else:
            lcs = lcs[1:]
    for el in first_dif:
        if first_dif.count(el) > 1:
            while el in first_dif:
                first_dif.remove(el)
    for el in second_dif:
        if second_dif.count(el) > 1:
            while el in second_dif:
                second_dif.remove(el)
    return (tuple(first_dif), tuple(second_dif))


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
    result = {}
    sentence_plagiarism = []
    sentence_lcs_length = []
    difference_indexes = []
    result['text_plagiarism'] = calculate_text_plagiarism_score(original_text_tokens,
                                                           suspicious_text_tokens,
                                                           plagiarism_threshold)
    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens = list(original_text_tokens)
        for i in range(len(original_text_tokens) - len(suspicious_text_tokens)):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)
    for i in range(len(suspicious_text_tokens)):
        first = original_text_tokens[i]
        second = suspicious_text_tokens[i]
        lcs = find_lcs(first, second, fill_lcs_matrix(first, second))
        sentence_plagiarism.append(calculate_plagiarism_score(len(lcs), second))
        sentence_lcs_length.append(find_lcs_length(first, second, plagiarism_threshold))
        difference_indexes.append(find_diff_in_sentence(first, second, lcs))
    result['sentence_plagiarism'] = sentence_plagiarism
    result['sentence_lcs_length'] = sentence_lcs_length
    result['difference_indexes'] = difference_indexes
    return result


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    if len(suspicious_text_tokens) > len(original_text_tokens):
        original_text_tokens = list(original_text_tokens)
        for i in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            original_text_tokens.append(())
        original_text_tokens = tuple(original_text_tokens)
    total_string = ''
    for i in range(len(suspicious_text_tokens)):
        fragment_string = '- '
        minus_str = ''
        for num, el in enumerate(original_text_tokens[i]):
            if num in accumulated_diff_stats['difference_indexes'][i][0]:
                minus_str += '| '
            minus_str += el + ' '
        if len(accumulated_diff_stats['difference_indexes'][i]) != minus_str.count('|') and minus_str.count('|') != 0:
            minus_str += '|'
        fragment_string += minus_str + '\n+ '
        plus_str = ''
        for num, el in enumerate(suspicious_text_tokens[i]):
            if num in accumulated_diff_stats['difference_indexes'][i][1]:
                plus_str += '| '
            plus_str += el + ' '
        if len(accumulated_diff_stats['difference_indexes'][i]) != plus_str.count('|') and plus_str.count('|') != 0:
            plus_str += '|'
        fragment_string += plus_str + '\n\n'
        fragment_string += 'lcs = '
        fragment_string += str(accumulated_diff_stats['sentence_lcs_length'][i]) + ', '
        fragment_string += 'plagiarism = ' + str(accumulated_diff_stats['sentence_plagiarism'][i] * 100) + '%'
        total_string += fragment_string + '\n\n'

    total_string += 'Text average plagiarism (words): ' + str(accumulated_diff_stats['text_plagiarism'] * 100) + '%'
    return total_string


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

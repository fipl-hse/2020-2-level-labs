"""
Longest common subsequence problem
"""
import json
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
    sentences = text.split('.')
    for sentence in sentences:
        # tokenized = [item for item in tokenize(sentence)]
        tokenized = list(tokenize(sentence))
        token = tuple(tokenized)
        if len(token) > 1:
            tokens.append(token)
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
    if isinstance(rows, int) and isinstance(columns, int) and not (isinstance(rows, bool) or isinstance(columns, bool)):
        if rows < 1 or columns < 1:
            return []
    else:
        return []
    matrix = []
    for _ in range(rows):
        row = [0 for _ in range(columns)]
        matrix.append(row)
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
    if not len(first_sentence_tokens) > 1 or not len(second_sentence_tokens) > 1:
        return []
    if not isinstance(first_sentence_tokens[0], str) or not isinstance(second_sentence_tokens[0], str):
        return []
    rows = len(first_sentence_tokens)
    columns = len(second_sentence_tokens)
    matrix = create_zero_matrix(rows, columns)
    if len(matrix) < 1:
        return []
    for row in range(rows):
        for column in range(columns):
            common = first_sentence_tokens[row] == second_sentence_tokens[column]
            matrix[row][column] = max(matrix[row-1][column], matrix[row][column-1])
            if common:
                matrix[row][column] += 1
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
    matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if not matrix:
        if first_sentence_tokens == () or second_sentence_tokens == ():
            return 0
        return -1
    if not isinstance(plagiarism_threshold, float):
        return -1
    if plagiarism_threshold > 1 or plagiarism_threshold < 0:
        return -1
    if matrix[-1][-1]/len(second_sentence_tokens) >= plagiarism_threshold:
        return matrix[-1][-1]
    return 0


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    row = -1
    column = -1
    c_s = []
    inputs = [(first_sentence_tokens, tuple, str, str),
              (second_sentence_tokens, tuple, str, str), (lcs_matrix, list, list, int)]
    for given_input in inputs:
        if not isinstance(given_input[0], given_input[1]):
            return ()
        if not len(given_input[0]) > 0:
            return ()
        if not isinstance(given_input[0][0], given_input[2]):
            return ()
        if not isinstance(given_input[0][0][0], given_input[3]):
            return ()
    if lcs_matrix[-1][-1] == 0 or not(lcs_matrix[0][0] == 1 or lcs_matrix[0][0] == 0):
        return ()
    while abs(row) <= len(first_sentence_tokens) or abs(column) <= len(second_sentence_tokens):
        if abs(column - 1) <= len(second_sentence_tokens):
            if lcs_matrix[row][column] == lcs_matrix[row][column - 1]:
                column = column - 1
                continue
        if abs(row - 1) <= len(first_sentence_tokens):
            if lcs_matrix[row][column] == lcs_matrix[row - 1][column]:
                row = row - 1
                continue
        c_s.append(first_sentence_tokens[row])
        row = row - 1
        column = column - 1
    return tuple(c_s[::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(lcs_length, int) or not isinstance(suspicious_sentence_tokens, tuple):
        return -1
    if not suspicious_sentence_tokens:
        return 0.0
    if len(suspicious_sentence_tokens) < lcs_length or lcs_length < 0 or isinstance(lcs_length, bool):
        return -1
    for token in suspicious_sentence_tokens:
        if not isinstance(token, str):
            return -1
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
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple):
        return -1
    if len(original_text_tokens) < len(suspicious_text_tokens):
        # original = [line for line in original_text_tokens]
        original = list(original_text_tokens)
        for _ in range(len(suspicious_text_tokens) - len(original_text_tokens)):
            original.append('')
        original_text_tokens = tuple(original)
    scores = []
    for i, tokens in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[i], tokens, plagiarism_threshold)
        scores.append(calculate_plagiarism_score(lcs_length, tokens))
    return sum(scores)/len(scores)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    def get_diff(sentence: list, lcs: tuple) -> tuple:
        length = len(sentence)
        basal_index = -1
        output = []
        for item in lcs:
            basal_index += 1
            splitted = ' '.join(sentence).split(item)
            chunk = splitted[0]
            if chunk:
                index_first = basal_index
                index_last = basal_index + len(chunk.split())
                output.extend([index_first, index_last])
            sentence = (item).join(splitted[1:]).split()
            if item == lcs[-1]:
                if sentence:
                    output.extend([length - len(sentence), length])
            basal_index = max(basal_index + len(chunk.split()), basal_index)
        return tuple(output)
    for given_input in [original_sentence_tokens, suspicious_sentence_tokens, lcs]:
        if not isinstance(given_input, tuple):
            return ()
        if len(given_input) > 0:
            if not isinstance(given_input[0], str):
                return ()
    if not lcs:
        output = []
        for sentence in [original_sentence_tokens, suspicious_sentence_tokens]:
            if not sentence:
                output.append(())
            else:
                output.append((0, len(sentence)))
        return tuple(output)
    output_first = get_diff(list(original_sentence_tokens), lcs)
    output_second = get_diff(list(suspicious_sentence_tokens), lcs)
    return (output_first, output_second)


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
    addition = ['' for _ in range(len(suspicious_text_tokens) - len(original_text_tokens))]
    if addition:
        original_text_tokens = list(original_text_tokens)
        original_text_tokens.extend(addition)
        original_text_tokens = tuple(original_text_tokens)
    stats = dict()
    stats['text_plagiarism'] = calculate_text_plagiarism_score(original_text_tokens,
                                                               suspicious_text_tokens,
                                                               plagiarism_threshold)
    for param in ['sentence_plagiarism', 'sentence_lcs_length', 'difference_indexes']:
        stats[param] = []
    for i, tokens in enumerate(suspicious_text_tokens):
        length = find_lcs_length(original_text_tokens[i], tokens, plagiarism_threshold)
        stats['sentence_plagiarism'].append(calculate_plagiarism_score(length, tokens))
        stats['sentence_lcs_length'].append(length)
        stats['difference_indexes'].append(find_diff_in_sentence(original_text_tokens[i], tokens,
        find_lcs(original_text_tokens[i], tokens, fill_lcs_matrix(original_text_tokens[i],
        tokens))))
    return stats


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    result = []
    length = accumulated_diff_stats['sentence_lcs_length']
    for i, item in enumerate(suspicious_text_tokens):
        lines = []
        try:
            for number, sentence in enumerate([original_text_tokens[i], item]):
                dif = accumulated_diff_stats['difference_indexes'][i][number]
                line = ''
                for index, word in enumerate(sentence):
                    if index in dif:
                        line += ' |'
                    line = line + ' ' + word
                if len(sentence) in dif:
                    line += ' |'
                lines.append(line)
            result.append(f'''- {lines[0]}
+ {lines[1]}

lcs = {length[i]}, plagiarism = {accumulated_diff_stats['sentence_plagiarism'][i] * 100}%''')
        except IndexError:
            result.append(f'''-
+ {' '.join(list(suspicious_text_tokens[i]))}

lcs = {length[i]}, plagiarism = {accumulated_diff_stats['sentence_plagiarism'][i] * 100}%\n''')
    result.append(f'Text average plagiarism (words): {accumulated_diff_stats["text_plagiarism"] * 100}%')
    print('\n'.join(result))
    return '\n'.join(result)


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
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple):
        return []
    if not len(first_sentence_tokens) > 1 or not len(second_sentence_tokens) > 1:
        return []
    if not isinstance(first_sentence_tokens[0], str) or not isinstance(second_sentence_tokens[0], str):
        return []
    lcs = 0
    for row in first_sentence_tokens:
        for column in second_sentence_tokens:
            if second_sentence_tokens[column] == first_sentence_tokens[row]:
                lcs += 1
    if lcs/len(second_sentence_tokens) < plagiarism_threshold:
        return 0
    return lcs


def get_tokens_id(path_to_file: str, i_d: dict, last_index: int) -> list:
    with open(path_to_file, encoding='utf-8') as file:
        tokens = []
        for line in file:
            addition = []
            for token in line.split():
                try:
                    addition.append(i_d[token])
                except KeyError:
                    i_d[token] = last_index + 1
                    addition.append(i_d[token])
                    last_index += 1
            tokens.extend(addition)
    return tuple(tokens)

def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    with open('indexes.json', 'r', encoding='utf-8') as file:
        i_d = json.load(file)
    return get_tokens_id(path_to_file, i_d, len(i_d))

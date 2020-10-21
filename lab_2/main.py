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
    if not isinstance(text, str) or not text:
        return ()
    tokens = []
    text = text.split('\n')
    for element in text:
        token = tuple(tokenize(element))
        if token:
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
    if not isinstance(rows, int) or not isinstance(columns, int)\
            or not rows > 0 or not columns > 0\
            or isinstance(rows, bool) or isinstance(columns, bool):
        return []
    zero_matrix = []
    for element in range(rows):
        zero_matrix += [[0 * element for element in range(columns)]]
    return zero_matrix



def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)\
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
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple)\
            or not isinstance(plagiarism_threshold, float) or None in first_sentence_tokens\
            or None in second_sentence_tokens or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1
    if len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
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
            or not isinstance(lcs_matrix, list) or not first_sentence_tokens\
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
    if not isinstance(lcs_length, int) or not isinstance(suspicious_sentence_tokens, tuple):
        return -1.0
    for element in suspicious_sentence_tokens:
        if not isinstance(element, str):
            return -1.0
    if not (not isinstance(lcs_length, bool) and isinstance(lcs_length, int)
            and 0 <= lcs_length <= len(suspicious_sentence_tokens)):
        return -1.0
    if not suspicious_sentence_tokens:
        return 0.0
    return lcs_length / len(suspicious_sentence_tokens)


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
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple):
        return -1.0
    plagiarism_score = []
    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += (()) * (len(suspicious_text_tokens) - len(original_text_tokens))
    if len(original_text_tokens) > len(suspicious_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]
    for index1, element1 in enumerate(original_text_tokens):
        for index2, element2 in enumerate(suspicious_text_tokens):
            if index1 == index2:
                lcs_length = find_lcs_length(element1, element2, plagiarism_threshold)
                plagiarism = calculate_plagiarism_score(lcs_length, element2)
                plagiarism_score.append(plagiarism)
    return sum(plagiarism_score) / len(suspicious_text_tokens)


def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    if not isinstance(original_sentence_tokens, tuple) or not isinstance(suspicious_sentence_tokens, tuple)\
            or not all(isinstance(i, str) for i in original_sentence_tokens)\
            or not all(isinstance(i, str) for i in suspicious_sentence_tokens)\
            or not isinstance(lcs, tuple) or not all(isinstance(i, str) for i in lcs):
        return ()
    different = []
    sentence = (original_sentence_tokens, suspicious_sentence_tokens)
    for element in sentence:
        dif = []
        for index, element1 in enumerate(element):
            if element1 not in lcs:
                if not index or element[index-1] in lcs:
                    dif.append(index)
                if index == len(element) - 1 or element[index+1] in lcs:
                    dif.append(index + 1)
        different.append(tuple(dif))
    return tuple(different)


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
    diff_stats = {'text_plagiarism': calculate_text_plagiarism_score(original_text_tokens,
                                                                     suspicious_text_tokens, plagiarism_threshold),
                  'sentence_plagiarism': [], 'sentence_lcs_length': [], 'difference_indexes': []}
    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += (()) * (len(suspicious_text_tokens) - len(original_text_tokens))
    if len(original_text_tokens) > len(suspicious_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]

    for element1, element2 in zip(original_text_tokens, suspicious_text_tokens):
        lcs_length = find_lcs_length(element1, element2, plagiarism_threshold)
        lcs_matrix = fill_lcs_matrix(element1, element2)
        lcs = find_lcs(element1, element2, lcs_matrix)
        diff_stats['sentence_lcs_length'].append(lcs_length)
        diff_stats['sentence_plagiarism'].append(calculate_plagiarism_score(lcs_length, element2))
        diff_stats['difference_indexes'].append(find_diff_in_sentence(element1, element2, lcs))
    return diff_stats


def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) \
            or not isinstance(accumulated_diff_stats, dict):
        return ''
    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += (()) * (len(suspicious_text_tokens) - len(original_text_tokens))
    if len(original_text_tokens) > len(suspicious_text_tokens):
        original_text_tokens = original_text_tokens[:len(suspicious_text_tokens)]

    text_plagiarism = accumulated_diff_stats['text_plagiarism'] * 100
    report = ''
    for element in range(len(suspicious_text_tokens)):
        difference = accumulated_diff_stats['difference_indexes'][element]
        suspicious = list(suspicious_text_tokens[element])
        original = list(original_text_tokens[element])
        counter = 0
        for index in difference[0]:
            suspicious.insert(index + counter, '|')
            original.insert(index + counter, '|')
            counter += 1
        suspicious = ''.join(suspicious)
        original = ''.join(original)
        lcs_length = accumulated_diff_stats['sentence_lcs_length'][element]
        plagiat = float(accumulated_diff_stats['sentence_plagiarism'][element] * 100)
        report += f'- {original}\n+ {suspicious}\n\nlcs = {lcs_length}, plagiarism = {plagiat}%\n\n'
    report += f'Text average plagiarism (words): {text_plagiarism}%'
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

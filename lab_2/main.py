"""
Longest common subsequence problem
"""
from lab_2 import tokenizer


def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """
    if not isinstance(text, str):  # проверка условий
        return ()
    text_sentences = text.split('\n')  # разделяем текст на предложения
    text_sentences_tokenize = []
    for sentence in text_sentences:  # добавляем в список кортежи предложений
        sentence_tokenize = tokenizer.tokenize(sentence)  # применяем функцию к одному предложению
        if sentence_tokenize:  # исключаем ошибку с пробелами и пустыми списками
            text_sentences_tokenize.append(tuple(sentence_tokenize))
    text_sentences_tokenize = tuple(text_sentences_tokenize)  # делаем из списка кортеж
    return text_sentences_tokenize


def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    wrong_circumstances = not isinstance(rows, int) or not isinstance(columns, int) \
     or isinstance(rows, bool) or isinstance(columns, bool) or rows <= 0 or columns <= 0
    if wrong_circumstances:
        return []
    zero_matrix = [[0 for index_col in range(columns)] for index_row in range(rows)]
    return zero_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    wrong_circumstances = not isinstance(first_sentence_tokens, tuple) \
                          or not isinstance(second_sentence_tokens, tuple) \
                          or first_sentence_tokens == () or second_sentence_tokens == () \
                          or None in first_sentence_tokens or None in second_sentence_tokens \
                          or isinstance(first_sentence_tokens, bool) \
                          or isinstance(second_sentence_tokens, bool)
    if wrong_circumstances:
        return []
    lcs_matrix = create_zero_matrix(len(first_sentence_tokens) + 1, len(second_sentence_tokens) + 1)
    for i in range(len(first_sentence_tokens)):
        for j in range(len(second_sentence_tokens)):
            if first_sentence_tokens[i] == second_sentence_tokens[j]:
                lcs_matrix[i + 1][j + 1] = lcs_matrix[i][j] + 1
            else:
                lcs_matrix[i + 1][j + 1] = max(lcs_matrix[i + 1][j], lcs_matrix[i][j + 1])
    lcs_matrix.remove(lcs_matrix[0]) #удаляем нулевую строку
    for element in lcs_matrix: #удаляем нулевой столбец
        element.remove(element[0])
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
    wrong_circumstances = not isinstance(first_sentence_tokens, tuple) \
                          or not isinstance(second_sentence_tokens, tuple) \
                          or isinstance(first_sentence_tokens, bool) \
                          or isinstance(second_sentence_tokens, bool) \
                          or not isinstance(plagiarism_threshold, float) \
                          or isinstance(plagiarism_threshold, bool) \
                          or plagiarism_threshold < 0 or plagiarism_threshold > 1 \
                          or None in first_sentence_tokens or None in second_sentence_tokens
    if wrong_circumstances:
        return -1
    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if first_sentence_tokens == () or second_sentence_tokens == () \
            or len(lcs_matrix) / len(second_sentence_tokens) < plagiarism_threshold:
        return 0
    else:
        return lcs_matrix[-1][-1]


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    wrong_circumstances = not isinstance(first_sentence_tokens, tuple) \
                          or not isinstance(second_sentence_tokens, tuple) \
                          or isinstance(first_sentence_tokens, bool) \
                          or isinstance(second_sentence_tokens, bool) \
                          or first_sentence_tokens == () or second_sentence_tokens == () \
                          or None in first_sentence_tokens or None in second_sentence_tokens \
                          or not isinstance(lcs_matrix, list) \
                          or isinstance(lcs_matrix, bool) \
                          or lcs_matrix == [] or None in lcs_matrix \
                          or (lcs_matrix[0][0] != 0 and lcs_matrix[0][0] != 1) \
                          or len(lcs_matrix) != len(first_sentence_tokens) \
                          or len(lcs_matrix[0]) != len(second_sentence_tokens)
    if wrong_circumstances:
        return ()
    for element in lcs_matrix:
        element.insert(0, 0)
    lcs_matrix.insert(0, [0] * (len(second_sentence_tokens) + 1))
    print(lcs_matrix)
    lcs = []
    i = len(first_sentence_tokens)
    j = len(second_sentence_tokens)
    while i != 0 and j != 0:
        if first_sentence_tokens[i - 1] == second_sentence_tokens[j - 1]:
            lcs.insert(0, first_sentence_tokens[i - 1])
            i = i - 1
            j = j - 1
        elif lcs_matrix[i - 1][j] > lcs_matrix[i][j - 1]:
            i = i - 1
        else:
            j = j - 1
    lcs = tuple(lcs)
    lcs_matrix.remove(lcs_matrix[0])  # удаляем нулевую строку
    for element in lcs_matrix:  # удаляем нулевой столбец
        element.remove(element[0])
    return lcs


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    wrong_circumstances = not isinstance(lcs_length, int) or isinstance(lcs_length, bool) \
                          or lcs_length < 0 \
                          or not isinstance(suspicious_sentence_tokens, tuple) \
                          or isinstance(suspicious_sentence_tokens, bool) \
                          or None in suspicious_sentence_tokens \
                          or (lcs_length > len(suspicious_sentence_tokens) \
                              and len(suspicious_sentence_tokens) != 0)
    if wrong_circumstances:
        return -1.0
    if len(suspicious_sentence_tokens) == 0:
        return 0.0
    plagiarism_score = lcs_length / len(suspicious_sentence_tokens)
    return plagiarism_score


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
    wrong_circumstances = not isinstance(original_text_tokens, tuple) \
                          or not isinstance(suspicious_text_tokens, tuple) \
                          or isinstance(original_text_tokens, bool) \
                          or isinstance(suspicious_text_tokens, bool) \
                          or (None,) in original_text_tokens \
                          or (None,) in suspicious_text_tokens \
                          or None in original_text_tokens or None in suspicious_text_tokens \
                          or not isinstance(plagiarism_threshold, float) \
                          or plagiarism_threshold < 0 or isinstance(plagiarism_threshold, bool) \
                          or plagiarism_threshold == None
    if wrong_circumstances:
        return -1.0
    plagiarism_score_sum = 0
    original_text_tokens = list(original_text_tokens)
    suspicious_text_tokens = list(suspicious_text_tokens)
    if len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens.extend(['' * (suspicious_text_tokens - original_text_tokens)])
    for index in range(len(suspicious_text_tokens)):
        lcs_length = find_lcs_length(original_text_tokens[index], suspicious_text_tokens[index],
                                     plagiarism_threshold=0.3)
        plagiarism_score = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[index])
        plagiarism_score_sum += plagiarism_score
    calculate_text_plagiarism_score = plagiarism_score_sum / len(suspicious_text_tokens)
    return calculate_text_plagiarism_score


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

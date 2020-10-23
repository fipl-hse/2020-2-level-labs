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
    
    sentences_in_text = text.split('\n')

    separate_sentences = []
    for sentence in sentences_in_text:
        if len(sentence) > 0:
            separate_sentences.append(tuple(tokenize(sentence)))
    separate_sentences = tuple(separate_sentences)

    return separate_sentences



def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    if (isinstance(rows, bool) or isinstance(columns, bool)) \
            or (rows == None or columns == None) \
            or (rows == [] or columns == []) or (rows == () or columns == ()) \
            or (rows == {} or columns == {}) or (rows == '' or columns == '') \
            or (isinstance(rows, float) or isinstance(columns, float)) \
            or (rows <= 0 or columns <= 0):

        return []

    matrix = [[0 for column in range(columns)] for row in range(rows)]

    return matrix




def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if isinstance(first_sentence_tokens, tuple) and isinstance(second_sentence_tokens, tuple) \
            and (first_sentence_tokens != (None, None) and second_sentence_tokens != (None, None)):

        lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

        for row_index, row_word in enumerate(first_sentence_tokens):
            for column_index, column_word in enumerate(second_sentence_tokens):

                if row_word == column_word:
                    lcs_matrix[row_index][column_index] = lcs_matrix[row_index - 1][column_index - 1] + 1

                else:
                    lcs_matrix[row_index][column_index] = max(lcs_matrix[row_index][column_index - 1],
                                                          lcs_matrix[row_index - 1][column_index])

        return lcs_matrix

    return []

def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    if isinstance(first_sentence_tokens, tuple) \
            and isinstance(second_sentence_tokens, tuple) \
            and (first_sentence_tokens != (None, None) and second_sentence_tokens != (None, None)) \
            and isinstance(plagiarism_threshold, float)  and (0 < plagiarism_threshold < 1):

        if len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
            return 0

        if len(first_sentence_tokens) > len(second_sentence_tokens):
            max_length = (fill_lcs_matrix(second_sentence_tokens, first_sentence_tokens))[-1][-1]
        else:
            max_length = (fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens))[-1][-1]

        fraction = max_length / len(second_sentence_tokens)
        if fraction < plagiarism_threshold:
            return 0

        return max_length

    return -1


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) \
            or not isinstance(second_sentence_tokens, tuple) \
            or not isinstance(lcs_matrix, list):
        return ()

    new_matrix = [[0] * len(lcs_matrix)]
    for elements_in_row in lcs_matrix:
        new_matrix.append([0] + elements_in_row)

    LCS = []
    row_index = len(first_sentence_tokens)
    column_index = len(second_sentence_tokens)

    while row_index >= 1 and column_index >= 1:

        if first_sentence_tokens[row_index - 1] == second_sentence_tokens[column_index - 1]:
            LCS.append(first_sentence_tokens[row_index - 1])
            row_index = row_index - 1
            column_index = column_index - 1

        elif new_matrix[row_index - 1][column_index] > new_matrix[row_index][column_index - 1]:
            row_index -= 1

        else:
            column_index -= 1
    LCS.reverse()

    return tuple(LCS)


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    pass


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
    pass


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

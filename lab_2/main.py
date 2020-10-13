"""
Longest common subsequence problem
"""

rows = 3
columns = 3


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
    if isinstance(rows, int) and isinstance(columns, int):
        for i in range(rows):
            zeros = [0] * columns
            matrix.append(zeros)
        # print(matrix)
        return matrix
    return []


# create_zero_matrix(rows, columns)

first_sentence_tokens = ('i', 'have', 'a', 'cat')
second_sentence_tokens = ('my', 'parents', 'have', 'a', 'cat', 'too')


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """

    is_tuple = isinstance(first_sentence_tokens, tuple) and isinstance(second_sentence_tokens, tuple)
    if is_tuple:

        for i, j in zip(first_sentence_tokens, second_sentence_tokens):
            is_none = (i is None) and (j is None)
            if not (isinstance(i, str) and isinstance(j, str)) or is_none:
                return []

        matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
        for left_i, left_elem in enumerate(first_sentence_tokens):  # y-axis
            for right_i, right_elem in enumerate(second_sentence_tokens):  # x-axis
                # matrix = create_zero_matrix(left_i, right_i)

                #is_bigger_zero = left_i > 0 and right_i > 0
                is_elem_equal = (left_elem == right_elem)

                if is_elem_equal:
                    matrix[left_i][right_i] = matrix[left_i - 1][right_i - 1] + 1

                else:
                    matrix[left_i][right_i] = max(matrix[left_i][right_i - 1], matrix[left_i - 1][right_i])
            # print(left_i, left_elem)
        print(matrix)
        return matrix
    return []


#fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)

plagiarism_threshold = 0.3
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
    lcs = []
    first_len = len(first_sentence_tokens) - 1  # 3
    second_len = len(second_sentence_tokens) - 1  # 5
    #print(first_len, second_len)  # delete
    while first_len >= 0 and second_len >= 0:
        if first_sentence_tokens[first_len] == second_sentence_tokens[second_len]:  # getting last tokens
            lcs.append(first_sentence_tokens[first_len])
            first_len -= 1
            second_len -= 1
        # print(first_len, second_len)
        elif matrix[first_len - 1][second_len] > matrix[first_len][second_len - 1]:
            first_len -= 1
        elif matrix[first_len - 1][second_len] <= matrix[first_len][second_len - 1]:
            second_len -= 1

    print(lcs)
    #return lcs_matrix
    len_lcs = len(lcs)
    len_second_s = len(second_sentence_tokens)
    print(len_lcs, len_second_s)
    ratio = len_lcs / len_second_s
    if ratio < plagiarism_threshold:
        print(0)
        return 0
    else:
        print(len_lcs)
        return len_lcs
find_lcs_length(first_sentence_tokens, second_sentence_tokens, plagiarism_threshold)

def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    pass


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    pass


def calculate_text_plagiarism_score(original_text_tokens: tuple, suspicious_text_tokens: tuple,
                                    plagiarism_threshold=0.3) -> float:
    """
    Calculates the plagiarism score: compares two texts line by line using lcs
    The score is the sum of lcs values for each pair divided by the number of tokens in suspicious text
    At the same time, a value of lcs is compared with a threshold (e.g. 0.3)
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param plagiarism_threshold: a threshold
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
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


def find_lcs_length_optimized(first_sentence_tokens: list, second_sentence_tokens: list) -> int:
    """
    Finds a length of the longest common subsequence using the Hirschberg's algorithm
    At the same time, if the first and last tokens coincide,
    they are immediately added to lcs and not analyzed
    :param first_sentence_tokens: a list of tokens
    :param second_sentence_tokens: a list of tokens
    :return: a length of the longest common subsequence
    """
    pass

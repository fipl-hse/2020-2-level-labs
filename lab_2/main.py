"""
Longest common subsequence problem
"""
import tokenizer

def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """

    tokens = ()

    if not isinstance(text, str):
        return ()
    sentences = text.split('\n')
    tokens = tuple(tuple(tokenizer.tokenize(sentence)) for sentence in sentences if tokenizer.tokenize(sentence))
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
    check = [isinstance(rows, int) and isinstance(columns, int) and not isinstance(rows, bool) and not isinstance(columns, bool)]
    if not all(check) or rows < 1 or columns < 1:
        return []

    matrix = []
    for row in range(rows):
        matrix.append([0*i for i in range(columns)])
    return matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    check = [isinstance(first_sentence_tokens, tuple), isinstance(second_sentence_tokens, tuple),
                  first_sentence_tokens, second_sentence_tokens,
                  len(first_sentence_tokens) != 0, len(second_sentence_tokens) != 0]

    if check and (isinstance(word, str) for word in first_sentence_tokens)\
            and (isinstance(word, str) for word in second_sentence_tokens):

        matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))

        for i, xi in enumerate(first_sentence_tokens):
            for j, yj in enumerate(second_sentence_tokens):
                if xi == yj:
                    if i < 0 or j < 0:
                        matrix[i][j] = 1
                    else:
                        matrix[i][j] = matrix[i - 1][j - 1] + 1
                else:
                    if i < 0 or j < 0:
                        matrix[i][j] = 1
                    else:
                        matrix[i][j] = max(matrix[i][j - 1], matrix[i - 1][j])
        return matrix
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
    check = [isinstance(first_sentence_tokens, tuple), isinstance(second_sentence_tokens, tuple),
                  first_sentence_tokens, second_sentence_tokens,
                  len(first_sentence_tokens) != 0, len(second_sentence_tokens) != 0,
                  (isinstance(word, str) for word in first_sentence_tokens),
                  (isinstance(word, str) for word in second_sentence_tokens)]

    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)

    if lcs_matrix == [] or not isinstance(plagiarism_threshold, float)\
            or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1
    elif len(lcs_matrix) / len(second_sentence_tokens) < plagiarism_threshold or len(second_sentence_tokens) == 0:
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
    fst_check = [isinstance(first_sentence_tokens, tuple), first_sentence_tokens,
                 len(first_sentence_tokens) != 0,
                 all(isinstance(word, str) for word in first_sentence_tokens)]
    sst_check = [isinstance(second_sentence_tokens, tuple), second_sentence_tokens,
                 len(second_sentence_tokens) != 0,
                 all(isinstance(word, str) for word in second_sentence_tokens)]
    matrix_check = [lcs_matrix, isinstance(lcs_matrix, list),
                    all(isinstance(i, list) for i in lcs_matrix),
                    all(isinstance(i, int) for lists in lcs_matrix for i in lists),
                    not all(isinstance(i, bool) for lists in lcs_matrix for i in lists),
                    lcs_matrix[0][0] in (0, 1),
                    len(lcs_matrix) == len(first_sentence_tokens),
                    len(lcs_matrix[0]) == len(second_sentence_tokens)]

    if not all(fst_check) or not all(sst_check) or not all(matrix_check):
        return ()

    row = len(lcs_matrix) - 1
    column = len(lcs_matrix[0]) - 1

    lcs = []

    while row or column:
        if first_sentence_tokens[row] == second_sentence_tokens[column]:
            lcs.append(first_sentence_tokens[row])
            row -= 1
            column -= 1
        elif lcs[row - 1][column] > lcs[row][column - 1] or not column:
            row -= 1
        else:
            column -= 1

    if first_sentence_tokens[0] == second_sentence_tokens[0]:
        lcs.append(first_sentence_tokens[0])

    return tuple(lcs[::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    check = [isinstance(lcs_length, int), not isinstance(lcs_length, bool),
             isinstance(suspicious_sentence_tokens, tuple),
             all(isinstance(i, str) for i in suspicious_sentence_tokens)]

    if isinstance(suspicious_sentence_tokens, tuple) and not suspicious_sentence_tokens:
        return 0
    if lcs_length > len(suspicious_sentence_tokens) > 0 or not check:
        return -1

    return lcs_length / len(suspicious_sentence_tokens)


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

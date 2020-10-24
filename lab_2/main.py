"""
Longest common subsequence problem
"""

def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """
    import tokenizer
    if not isinstance(text, str):
        return ()
    else:
        all_lines = []
        text2 = text.split('\n')
        for sent in text2:
            sent2 = tokenizer.tokenize(sent)
            if len(sent2) != 0:
                all_lines.append(tuple(sent2))
    all_lines2 = tuple(all_lines)
    return all_lines2

def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    check_bool = (isinstance(rows, bool) or isinstance(columns, bool))
    if not isinstance(rows, int) or not isinstance(columns, int) or check_bool:
        return []
    elif rows < 1 or columns < 1:
        return []

    zero_matrix = [[0 for column in range(columns)] for row in range(rows)]
    return zero_matrix



def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple):
        return []

    for token1 in first_sentence_tokens:
        if not isinstance(token1, str):
            return []
    for token2 in second_sentence_tokens:
        if not isinstance(token2, str):
            return []

    rows, columns = len(first_sentence_tokens), len(second_sentence_tokens)
    lcs_matrix = create_zero_matrix(rows, columns)
    for i, el_1 in enumerate(first_sentence_tokens):
        for j, el_2 in enumerate(second_sentence_tokens):
            if el_1 == el_2 and i == j:
                lcs_matrix[i][j] = lcs_matrix[i - 1][j - 1] + 1
            else:
                lcs_matrix[i][j] = max(lcs_matrix[i - 1][j], lcs_matrix[i][j - 1])
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
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple):
        return -1

    for words_1 in first_sentence_tokens:
        if not isinstance(words_1, str) or not words_1:
            return -1
    for words_2 in second_sentence_tokens:
        if not isinstance(words_2, str) or not words_2:
            return -1

    if not isinstance(plagiarism_threshold, float) or not (0 <= plagiarism_threshold <= 1):
        return -1


    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)

    if not lcs_matrix:
        return 0
    lcs_length = lcs_matrix[-1][-1]
    length_sec_sent = len(second_sentence_tokens)
    if lcs_length/length_sec_sent < plagiarism_threshold:
        return 0
    else:
        return lcs_length




def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple):
        return ()

    for words_1 in first_sentence_tokens:
        if not isinstance(words_1, str) or not words_1:
            return ()
    for words_2 in second_sentence_tokens:
        if not isinstance(words_2, str) or not words_2:
            return ()

    if not isinstance(lcs_matrix, list) or not lcs_matrix or not first_sentence_tokens or not second_sentence_tokens:
        return ()

    length1 = len(first_sentence_tokens)
    length2 = len(second_sentence_tokens)
    if len(lcs_matrix) != length1 or len(lcs_matrix[0]) != length2:
        return ()

    if lcs_matrix[0][0] != 0 and lcs_matrix[0][0] != 1:
        return ()

    lcs = []
    for i_r, all_row in enumerate(reversed(lcs_matrix)):
        for i_c, el_col in enumerate(reversed(all_row)):
            if all_row and el_col:
                if first_sentence_tokens[i_r] == second_sentence_tokens[i_c]:
                    lcs.append(second_sentence_tokens[i_c])
    return tuple(lcs)



def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(lcs_length, int) or not isinstance(suspicious_sentence_tokens, tuple) or\
               None in suspicious_sentence_tokens or isinstance(lcs_length, bool):
        return -1.0

    for token in suspicious_sentence_tokens:
        if not isinstance(token, str):
            return -1.0

    num_tokens = len(suspicious_sentence_tokens)
    if num_tokens == 0:
        return 0.0
    plagiarism_score = lcs_length / num_tokens
    if not (0 <= plagiarism_score <= 1):
        return -1.0
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
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple):
        return -1.0
    if not original_text_tokens or not suspicious_text_tokens:
        return -1.0

    for sent1 in original_text_tokens:
        if not isinstance(sent1, tuple):
            return -1.0
        for word1 in sent1:
            if not isinstance(word1, str):
                return -1.0
    for sent2 in suspicious_text_tokens:
        if not isinstance(sent2, tuple):
            return -1.0
        for word2 in sent2:
            if not isinstance(word2, str):
                return -1.0

    length1 = len(original_text_tokens)
    length2 = len(suspicious_text_tokens)
    if length1 < length2:
        original_text_tokens += (() * (length2 - length1))
    elif length2 < length1:
        original_text_tokens = original_text_tokens[:length2]

    p_sum = 0
    for sent in range(len(original_text_tokens)):
        lcs_length = find_lcs_length(original_text_tokens[sent], suspicious_text_tokens[sent], plagiarism_threshold)
        if lcs_length == -1.0:
            return -1.0
        p_sent = calculate_plagiarism_score(lcs_length, suspicious_text_tokens[sent])
        if p_sent == -1:
            p_sent = 0.0
        p_sum += p_sent

    p_result = p_sum / len(suspicious_text_tokens)
    return p_result





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

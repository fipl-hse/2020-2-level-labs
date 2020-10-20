"""
Longest common subsequence problem
"""
import copy
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
    for index in range(0, len(text)):
        if len(text[index]) != 0:
            text[index] = tuple(text[index].split())
        else:
            text.remove(text[index])
    return tuple(text)



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
    row_pattern = [0] * columns
    counter = 0
    while counter < rows:
        zero_matrix.append(copy.deepcopy(row_pattern))
        counter += 1
    return zero_matrix


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if not isinstance (first_sentence_tokens, tuple) or not isinstance (second_sentence_tokens, tuple):
        return []
    if len(first_sentence_tokens) == 0 or len(second_sentence_tokens) == 0:
        return []
    for word in first_sentence_tokens:
        if not isinstance (word, str):
            return []
    for word in second_sentence_tokens:
        if not isinstance (word, str):
            return []
    matrix = create_zero_matrix(len(first_sentence_tokens) + 1, len(second_sentence_tokens) + 1)
    new_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
    row_counter = 0
    for row in matrix:
        if row_counter != 0:
            column_counter = 0
            for column in row:
                if column_counter != 0:
                    if first_sentence_tokens[row_counter - 1] == second_sentence_tokens[column_counter - 1]:
                        matrix[row_counter][column_counter] = matrix[row_counter - 1][column_counter - 1] + 1
                        new_matrix[row_counter - 1][column_counter - 1] = matrix[row_counter][column_counter]
                    else:
                        matrix[row_counter][column_counter] = (max(matrix[row_counter][column_counter - 1],
                            matrix[row_counter - 1][column_counter]))
                        new_matrix[row_counter - 1][column_counter - 1] = matrix[row_counter][column_counter]
                column_counter += 1
        row_counter += 1
    return new_matrix


def find_lcs_length(first_sentence_tokens: tuple, second_sentence_tokens: tuple, plagiarism_threshold: float) -> int:
    """
    Finds a length of the longest common subsequence using the Needleman–Wunsch algorithm
    When a length is less than the threshold, it becomes 0
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param plagiarism_threshold: a threshold
    :return: a length of the longest common subsequence
    """
    if not isinstance (first_sentence_tokens, tuple) or not isinstance (second_sentence_tokens, tuple):
        return -1
    for word in first_sentence_tokens:
        if not isinstance (word, str):
            return -1
    for word in second_sentence_tokens:
        if not isinstance (word, str):
            return -1
    if not isinstance(plagiarism_threshold, float):
        return -1
    if not 0 < plagiarism_threshold <= 1:
        return -1
    matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if len (matrix) > 0:
        result = matrix[-1][-1]
    else:
        result = 0
    if len(second_sentence_tokens) == 0:
        return 0
    if result/len(second_sentence_tokens) < plagiarism_threshold:
        return 0
    else:
        return result


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance (second_sentence_tokens, tuple):
        return ()
    for word in first_sentence_tokens:
        if not isinstance(word, str):
            return ()
    for word in second_sentence_tokens:
        if not isinstance(word, str):
            return ()
    if not isinstance(lcs_matrix, list):
        return ()
    if len(lcs_matrix) == 0:
        return ()
    for row in lcs_matrix:
        if not isinstance (row, list):
            return ()
        for column in row:
            if not isinstance (column, int):
                return ()
    if not len(first_sentence_tokens) == len (lcs_matrix):
        return ()
    for row in lcs_matrix:
        if len(row) != len (second_sentence_tokens):
            return ()
    if lcs_matrix != fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens):
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
    if not isinstance(lcs_length, int):
        return -1
    if lcs_length < 0:
        return -1
    if lcs_length > len(suspicious_sentence_tokens):
        return -1
    if isinstance (lcs_length, bool):
        return -1
    for word in suspicious_sentence_tokens:
        if not isinstance (word, str):
            return -1
    plagiarism_score = lcs_length/len(suspicious_sentence_tokens)
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
    if not isinstance (original_text_tokens, tuple) or not isinstance (suspicious_text_tokens, tuple):
        return -1
    for sentence in original_text_tokens:
        if not isinstance(sentence, tuple):
            return -1
        for word in sentence:
            if not isinstance(word, str):
                return -1
    for sentence in suspicious_text_tokens:
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
    while len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens = list (original_text_tokens)
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
    if not isinstance (original_sentence_tokens, tuple) or not isinstance (suspicious_sentence_tokens, tuple):
        return ()
    if not isinstance (lcs, tuple):
        return ()
    for word in original_sentence_tokens:
        if not isinstance (word, str):
            return ()
    for word in suspicious_sentence_tokens:
        if not isinstance (word, str):
            return ()
    for word in lcs:
        if not isinstance (word, str):
            return ()
    first_list = []
    second_list = []
    flag = 'closed'
    for word in original_sentence_tokens:
        if word not in lcs and flag == 'closed':
            first_list.append(original_sentence_tokens.index(word))
            flag = 'opened'
        elif word in lcs and flag == 'opened':
            first_list.append(original_sentence_tokens.index(word))
            flag = 'closed'
        if word not in lcs and original_sentence_tokens.index(word) == len(original_sentence_tokens) - 1:
            first_list.append(len(original_sentence_tokens))
    flag = 'closed'
    for word in suspicious_sentence_tokens:
        if word not in lcs and flag == 'closed':
            second_list.append(suspicious_sentence_tokens.index(word))
            flag = 'opened'
        elif word in lcs and flag == 'opened':
            second_list.append(suspicious_sentence_tokens.index(word))
            flag = 'closed'
        if word not in lcs and suspicious_sentence_tokens.index(word) == len(suspicious_sentence_tokens) - 1:
            second_list.append(len(suspicious_sentence_tokens))
    result = (tuple(first_list), tuple(second_list))
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
    for sentence in original_text_tokens:
        if not isinstance(sentence, tuple):
            return {}
        for word in sentence:
            if not isinstance(word, str):
                return {}
    for sentence in suspicious_text_tokens:
        if not isinstance(sentence, tuple):
            return {}
        for word in sentence:
            if not isinstance(word, str):
                return {}
    if not isinstance(plagiarism_threshold, float):
        return {}
    if not 0 <= plagiarism_threshold <= 1:
        return {}
    text_plagiarism = calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens, plagiarism_threshold)
    sentence_plagiarism = []
    sentence_lcs_length = []
    difference_indexes = []
    for sent_1, sent_2 in zip(original_text_tokens, suspicious_text_tokens):
        lcs_length = find_lcs_length(sent_1, sent_2, plagiarism_threshold)
        sentence_lcs_length.append(lcs_length)
        plagiarism_score = calculate_plagiarism_score(lcs_length, sent_2)
        lcs_matrix = fill_lcs_matrix(sent_1, sent_2)
        lcs = find_lcs(sent_1, sent_2, lcs_matrix)
        sent_diff = find_diff_in_sentence(sent_1, sent_2, lcs)
        if plagiarism_score == -1:
            plagiarism_score = 0
        sentence_plagiarism.append(plagiarism_score)
        difference_indexes.append(sent_diff)
    return {'text_plagiarism': text_plagiarism, 'sentence_plagiarism': sentence_plagiarism,
            'sentence_lcs_length': sentence_lcs_length, 'difference_indexes': difference_indexes}

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
    for sentence in original_text_tokens:
        if not isinstance(sentence, tuple):
            return ''
        for word in sentence:
            if not isinstance(word, str):
                return ''
    for sentence in suspicious_text_tokens:
        if not isinstance(sentence, tuple):
            return ''
        for word in sentence:
            if not isinstance(word, str):
                return ''
    if not isinstance (accumulated_diff_stats, dict):
        return ''
    new_orig = []
    new_susp = []
    result = []
    difference_indexes = accumulated_diff_stats.get('difference_indexes')
    original_text_tokens = list(original_text_tokens)
    for sent_1, subtuple in zip(original_text_tokens, difference_indexes):
        sent_1 = list(sent_1)
        i = 0
        for index in subtuple[0]:
            if len(subtuple[0]) != 0:
                sent_1.insert(index + i, '|')
                i += 1
        sent_1 = ' '.join(sent_1)
        new_orig.append(sent_1)
    suspicious_text_tokens = list(suspicious_text_tokens)
    for sent_2, subtuple in zip(suspicious_text_tokens, difference_indexes):
        sent_2 = list(sent_2)
        i = 0
        for index in subtuple[1]:
            if len(subtuple[1]) != 0:
                sent_2.insert(index + i, '|')
                i += 1
        sent_2 = ' '.join(sent_2)
        new_susp.append(sent_2)
    for sent_1, sent_2 in zip(new_orig, new_susp):
        lcs = accumulated_diff_stats.get('sentence_lcs_length')[new_orig.index(sent_1)]
        plagiarism = str(accumulated_diff_stats.get('sentence_plagiarism')[new_orig.index(sent_1)] * 100) + '%'
        average_plag = str(accumulated_diff_stats.get('text_plagiarism') * 100) + '%'
        current_result = ('-', sent_1, '\n' + '+', sent_2, '\n\n' + 'lcs =',
               str(lcs) + ',', 'plagiarism =', plagiarism, '\n\n')
        current_result = ' '.join(current_result)
        result.append(current_result)
    current_result2 = ('Text average plagiarism (words):', average_plag, '\n')
    current_result2 = ' '.join(current_result2)
    result.append(current_result2)
    result = ''.join(result)
    return result
create_diff_report((('i', 'have', 'a', 'cat'), ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur')), (('i', 'have', 'a', 'cat'),('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur')), accumulate_diff_stats((('i', 'have', 'a', 'cat'), ('its', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur')), (('i', 'have', 'a', 'cat'),('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur'))))

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

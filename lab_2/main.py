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
    if not isinstance(text, str) or not text:
        return ()
    sentences = text.split('\n')
    list_lines = []
    for sentence in sentences:
        if sentence != '' and len(tokenize(sentence)):
           tokens = tuple (tokenize(sentence))  # кортеж из каждого предложения
           list_lines.append (tokens)
    return tuple(list_lines)

def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    is_bool_rows = isinstance(rows, bool)
    is_bool_columns = isinstance(columns, bool)
    is_not_int_rows = not isinstance(rows, int)
    is_not_int_columns = not isinstance(columns, int)

    if is_bool_rows or is_bool_columns or is_not_int_rows or is_not_int_columns or rows <= 0 or columns <= 0:
        return []

    return [[0 for column in range(columns)] for row in range(rows)]  # создание 0 двумерного массива


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if (not isinstance(first_sentence_tokens, tuple)
            or not isinstance(second_sentence_tokens, tuple)
            or not all(isinstance(i, str) for i in first_sentence_tokens)
            or not all(isinstance(i, str) for i in second_sentence_tokens)):
        return []

    lcs_matrix = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))  # r & c  по длинам
    for in_1, elem_1 in enumerate(first_sentence_tokens):
        for in_2, elem_2 in enumerate(second_sentence_tokens):
            if elem_1 == elem_2:
                lcs_matrix[in_1][in_2] = lcs_matrix[in_1 - 1][in_2 - 1] + 1
            else:
                lcs_matrix[in_1][in_2] = max(lcs_matrix[in_1][in_2 - 1], lcs_matrix[in_1 - 1][in_2])
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
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
          or not isinstance(plagiarism_threshold, float) or None in first_sentence_tokens \
          or None in second_sentence_tokens or plagiarism_threshold < 0 or plagiarism_threshold > 1:
        return -1

    if len(first_sentence_tokens) == 0 or not first_sentence_tokens \
            or len(second_sentence_tokens) == 0 or not second_sentence_tokens:
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
            or not isinstance(lcs_matrix, list) or not first_sentence_tokens \
            or not second_sentence_tokens or not lcs_matrix or None in lcs_matrix:
        return ()

    if lcs_matrix:
        if len(lcs_matrix) == len(first_sentence_tokens) and len(lcs_matrix[0]) == len(second_sentence_tokens):
            if lcs_matrix[0][0] > 1:
                return ()
    max_len = []
    for ind_1, el_1 in enumerate(reversed(lcs_matrix)):
        for ind_2, el_2 in enumerate(reversed(el_1)):
            if not el_1 or not el_2:
                return ()
            if first_sentence_tokens[ind_1] == second_sentence_tokens[ind_2]:
                max_len.append(second_sentence_tokens[ind_2])
    return tuple(max_len)

def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(suspicious_sentence_tokens, tuple):
        return -1.0
    if not suspicious_sentence_tokens:
        return 0.0
    for word in suspicious_sentence_tokens:
        if not isinstance(word, str):
            return -1.0
    if not isinstance(lcs_length, int) or isinstance(lcs_length, bool) or lcs_length < 0:
        return -1.0
    if lcs_length > len(suspicious_sentence_tokens):
        return -1.0

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
    check_orig = (not isinstance(original_text_tokens, tuple)
                      or not all(isinstance(i, tuple) for i in original_text_tokens)
                      or not all(isinstance(i, str) for tokens in original_text_tokens for i in tokens))

    check_susp = (not isinstance(suspicious_text_tokens, tuple)
                        or not all(isinstance(i, tuple) for i in suspicious_text_tokens)
                        or not all(isinstance(i, str) for tokens in suspicious_text_tokens for i in tokens))

    check_threshold = (not isinstance(plagiarism_threshold, float)
                       or not 0 < plagiarism_threshold < 1)

    if check_orig or check_susp or check_threshold:
        return -1

    if ((isinstance(original_text_tokens, tuple) and not any(original_text_tokens))
            or (isinstance(suspicious_text_tokens, tuple) and not any(suspicious_text_tokens))):
        return 0

    while len(original_text_tokens) < len(suspicious_text_tokens):
        original_text_tokens += ('',)

    score_all = 0
    for i, susp_sent in enumerate(suspicious_text_tokens):
        lcs_length = find_lcs_length(original_text_tokens[i],susp_sent, plagiarism_threshold) #отношение к длине
        
        score = calculate_plagiarism_score(lcs_length,susp_sent)    #колво плагиата построчно
        score_all += score
    return score_all / len(suspicious_text_tokens)

def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    if not isinstance(original_sentence_tokens, tuple) or not\
            isinstance(suspicious_sentence_tokens, tuple) or not isinstance(lcs, tuple):
        return ()
    if None in original_sentence_tokens or None in suspicious_sentence_tokens or None in lcs:
        return ()

    suspicious_indexes = []
    for ind, elem in enumerate(suspicious_sentence_tokens):  # незначительные схожести
        if elem not in lcs:
            suspicious_indexes.append(ind)  #индексы в предложение

    diff_indexes = []
    for number, index in enumerate(suspicious_indexes):    
        if len(suspicious_indexes) - 1 != number:
            if index + 1 != suspicious_indexes[number + 1]:
                diff_indexes.extend([index, index + 1])
            elif index - 1 not in suspicious_indexes and index + 1 in suspicious_indexes:   
                diff_indexes.append(index)
            elif index - 1 in suspicious_indexes and index + 1 not in suspicious_indexes:
                diff_indexes.append(index + 1)

        elif len(suspicious_indexes) - 1 == number:     
            if index - 1 != suspicious_indexes[number - 1]:
                diff_indexes.extend([index, index + 1])
            elif index - 1 == suspicious_indexes[number - 1]:
                diff_indexes.append(index + 1)
    if original_sentence_tokens == ():
        return tuple([(), tuple(diff_indexes)])
    return tuple([tuple(diff_indexes), tuple(diff_indexes)])

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
    is_type_incorrect = not isinstance(original_text_tokens, tuple) or \
                        not isinstance(suspicious_text_tokens, tuple) or not\
                        isinstance(plagiarism_threshold, float) \
                        or not 0 <= plagiarism_threshold <= 1
    if is_type_incorrect or original_text_tokens is None or suspicious_text_tokens is None:
        return {}

    length = len(suspicious_text_tokens)
    while len(original_text_tokens) < length:   #equal length
        original_text_tokens += ('',)

    all_states = {'text_plagiarism': 0,
            'sentence_plagiarism': [0] * length,
            'sentence_lcs_length': [0] * length,
            'difference_indexes': [0] * length}

    orig = original_text_tokens
    susp = suspicious_sentence_tokens
    pl_thr = plagiarism_threshold
    all_states['text_plagiarism'] = calculate_text_plagiarism_score(orig, susp, pl_thr)
    for i in range(length):
        lcs_length = find_lcs_length(orig[i], susp[i],  pl_thr=0.0)      #предложений несколько/ посдчет заиствований в отдельных ключах

        all_states['sentence_plagiarism'][i] = calculate_plagiarism_score(lcs_length, susp[i])
        all_states ['sentence_lcs_length'] [i]= lcs_length

        lcs_matrix = fill_lcs_matrix(orig[i], susp[i])
        lcs = find_lcs(orig[i], susp[i], lcs_matrix)
        all_states['difference_indexes'][i]= find_diff_in_sentence(orig[i], susp[i],lcs)
    return all_states

def create_diff_report(original_text_tokens: tuple, suspicious_text_tokens: tuple, accumulated_diff_stats: dict) -> str:
    """
    Creates a diff report for two texts comparing them line by line
    :param original_text_tokens: a tuple of sentences with tokens
    :param suspicious_text_tokens: a tuple of sentences with tokens
    :param accumulated_diff_stats: a dictionary with statistics for each pair of sentences
    :return: a report
    """
    if not isinstance(original_text_tokens, tuple) or not isinstance(suspicious_text_tokens, tuple) or not isinstance(accumulated_diff_stats, dict):
        return ''

    length = len(suspicious_text_tokens)
    while len(original_text_tokens) < length:
        original_text_tokens += ('',)
    report = ''

    for ind in range(len(original_text_tokens)):
        sent_1 = list(original_text_tokens[ind])
        sent_2 = list(suspicious_text_tokens[ind])
        diff_indexes = accumulated_diff_stats['difference_indexes'][ind]

        index = 0
        for i in diff_indexes[0]:
            sent_1.insert(i + index, '|')
            sent_2.insert(i + index, '|')
            index += 1
        orig_sent = ' '.join(sent_1)
        susp_sent = ' '.join(sent_2)
    
        matrix = accumulated_diff_stats['sentence_lcs_length'][ind]
        plag_score = float(accumulated_diff_stats['sentence_plagiarism'][ind] * 100)

        report += '- {}\n+ {}\n\nlcs = {}, plagiarism = {}%\n\n'.format(orig_sent,susp_sent,matrix,plag_score)    
    text_plagiarism = float(accumulated_diff_stats['text_plagiarism'] * 100)
    report += 'Text average plagiarism (words): {}%'.format(text_plagiarism)
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
    return 0

def tokenize_big_file(path_to_file: str) -> tuple:
    """
    Reads, tokenizes and transforms a big file into a numeric form
    :param path_to_file: a path
    :return: a tuple with ids
    """
    return ()
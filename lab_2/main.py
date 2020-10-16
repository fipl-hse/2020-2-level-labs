"""
Longest common subsequence problem
"""

rows = 3
columns = 0


# bad_inputs = [[], {}, (), '', 9.22, -1, 0, -6, None, True]

text = 'My cat is Bruno\nHe is so smart'
def tokenize_by_lines(text: str) -> tuple:
    """
    Splits a text into sentences, sentences – into tokens,
    converts the tokens into lowercase, removes punctuation
    :param text: the initial text
    :return: a list of sentences with lowercase tokens without punctuation
    e.g. text = 'I have a cat.\nHis name is Bruno'
    --> (('i', 'have', 'a', 'cat'), ('his', 'name', 'is', 'bruno'))
    """
    from tokenizer import tokenize

    if isinstance(text, str):
        new_textt = []
        #for i in text:
        new_text = text.split('\n')
        print(new_text)
        for i in new_text:
            token = tokenize(i)
            tokens = new_textt.append(token)
            #if text[i:i+1] == '\n':
            #tez = text[:i]
            #new_token = tuple(token)
            #new_text.append(new_token)
        print(tokens)
#tokenize_by_lines(text)

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

    is_int = isinstance(rows, int) and isinstance(columns, int)
    is_not_none = rows is not None or columns is not None
    is_bool = isinstance(rows, bool) or isinstance(columns, bool)

    if is_int and is_not_none and not is_bool and (rows > 0 and columns > 0):
        for i in range(rows):
            zeros = [0] * columns
            matrix.append(zeros)
        return matrix

    return []


create_zero_matrix(rows, columns)

first_sentence_tokens = ('the', 'dog', 'is', 'running')  # ('i', 'have', 'a', 'cat')
second_sentence_tokens = ('the', 'cat', 'is', 'sleeping')  # ('my', 'parents', 'have', 'a', 'cat', 'too')


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

        f = create_zero_matrix(len(first_sentence_tokens), len(second_sentence_tokens))
        for i, i_elem in enumerate(first_sentence_tokens):
            for j, j_elem in enumerate(second_sentence_tokens):
                if i_elem == j_elem:
                    f[i][j] = f[i - 1][j - 1] + 1
                else:
                    f[i][j] = max(f[i][j - 1], f[i - 1][j])
        return f

    return []


fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)

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

    is_tuple = isinstance(first_sentence_tokens, tuple) and isinstance(second_sentence_tokens, tuple)
    is_pos_float = (isinstance(plagiarism_threshold, float)) and (1 > plagiarism_threshold > 0)
    if is_tuple and is_pos_float:

        for i, j in zip(first_sentence_tokens, second_sentence_tokens):
            is_none = (i is None) and (j is None)
            if not (isinstance(i, str) and isinstance(j, str)) or is_none:
                return -1

        matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
        len_lcs = matrix[-1][-1]
        len_second_s = len(second_sentence_tokens)
        ratio = len_lcs / len_second_s
        if ratio < plagiarism_threshold:
            # print(0)
            return 0
        else:
            # print(len_lcs)
            return len_lcs
    # print(-1)
    return -1


# find_lcs_length(first_sentence_tokens, second_sentence_tokens, plagiarism_threshold)

lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)  # delete


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> list:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    lcs = []

    is_tuple = isinstance(first_sentence_tokens, tuple) and isinstance(second_sentence_tokens, tuple)
    if is_tuple:

        for i, j in zip(first_sentence_tokens, second_sentence_tokens):
            is_none = i is None and j is None
            if not (isinstance(i, str) and isinstance(j, str)) or is_none:
                # print([])
                return []

        if isinstance(lcs_matrix, list) and bool(lcs_matrix) is True:
            for k in lcs_matrix:  # here
                if isinstance(k, list):
                    for num in k:
                        is_num = isinstance(num, int) and num > 0
                        # is_true = any(k) or any(num)
                        is_none = k is None or num is None

                        if not is_num or is_none or k is False or num is False:
                            print(())
                            return ()
                    # return ()

                    i_len = len(first_sentence_tokens) - 1  # 3
                    j_len = len(second_sentence_tokens) - 1
                    while i_len >= 0 and j_len >= 0:

                        if first_sentence_tokens[i_len - 1] == second_sentence_tokens[j_len - 1]:
                            lcs.append(first_sentence_tokens[i_len - 1])
                            i_len -= 1
                            j_len -= 1

                        elif lcs_matrix[i_len - 1][j_len] == lcs_matrix[i_len][j_len]:
                            i_len -= 1

                        else:
                            j_len -= 1

                    lcs.reverse()
                    lcs = tuple(lcs)

                    return lcs

                return ()

        return ()

    return []


# find_lcs(first_sentence_tokens, second_sentence_tokens, lcs_matrix)

lcs_length = 3
suspicious_sentence_tokens = (('the', 'man', 'arrived'),
                              ('the', 'boy', 'left'))


# suspicious_sentence_tokens = ('', '', None)
# bad_inputs = [[], {}, (), 9.22, -1, 0, -6, None, True]
def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    is_tuple = isinstance(suspicious_sentence_tokens, tuple) and bool(suspicious_sentence_tokens) is True
    is_int = isinstance(lcs_length, int) and not isinstance(lcs_length, bool)

    if is_int and lcs_length >= 0 and is_tuple and (lcs_length <= 100):
        for i in suspicious_sentence_tokens:
            if isinstance(i, str) and i != '':
                score = lcs_length / len(suspicious_sentence_tokens)
                print(score)
                return score
            # print(-1)
            return -1
    # print(-1)
    return -1


#calculate_plagiarism_score(lcs_length, suspicious_sentence_tokens)

# original_text_tokens = (('the', 'cat', 'appeared'),
                        # ('the', 'dog', 'disappeared'))
# suspicious_text_tokens = (('the', 'man', 'arrived'),
                          # ('the', 'boy', 'left'))


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
    #plagiarism = calculate_plagiarism_score(lcs_length, suspicious_sentence_tokens) # is it even correct..

    len_orig = len(original_text_tokens)
    len_susp = len(suspicious_text_tokens)
    print(len_susp)
    empty_tuple = ()

    #for i, j in zip(original_text_tokens, suspicious_text_tokens):

    if len_orig < len_susp:
        new_orig_text = original_text_tokens + empty_tuple
    elif len_orig > len_susp:
        new_orig_text = original_text_tokens[:len_susp + 1]  #do it with enumerate.....
    elif len_orig == len_susp:
        new_orig_text = original_text_tokens

    print(new_orig_text)
    for orig_s, susp_s in zip(new_orig_text, suspicious_text_tokens):
        lcs_len = find_lcs_length(orig_s, susp_s, plagiarism_threshold)
    print(suspicious_text_tokens)

    p_res = 0.0

    for i in suspicious_text_tokens:
        plagiarism = calculate_plagiarism_score(lcs_len, i)
        p_res += plagiarism
    #print(suspicious_text)
    p_result = p_res / len_susp
    print(p_result)

#calculate_text_plagiarism_score(original_text_tokens, suspicious_text_tokens, plagiarism_threshold=0.3)


original_sentence_tokens = ('itss', 'body', 'is', 'covered', 'with', 'bushy', 'white', 'fur')
suspicious_sentence_tokens = ('its', 'body', 'is', 'covered', 'with', 'shiny', 'black', 'fur')
lcs = ('its', 'body', 'is', 'covered', 'with', 'fur')

def find_diff_in_sentence(original_sentence_tokens: tuple, suspicious_sentence_tokens: tuple, lcs: tuple) -> tuple:
    """
    Finds words not present in lcs.
    :param original_sentence_tokens: a tuple of tokens
    :param suspicious_sentence_tokens: a tuple of tokens
    :param lcs: a longest common subsequence
    :return: a tuple with tuples of indexes
    """
    orig_indices = []
    susp_indices = []
    all_indices = []

    for index, (original, suspect) in enumerate(zip(original_sentence_tokens, suspicious_sentence_tokens)):
        if original != suspect and index == 0:
            orig_indices.append(index)
            susp_indices.append(index)
            orig_indices.append(index + 1)
            susp_indices.append(index + 1)
        elif original != suspect and original_sentence_tokens[index + 1:] not in lcs:
            orig_indices.append(index)
            susp_indices.append(index)
        elif (original != suspect and original_sentence_tokens[index + 1:] != -1 and
              original_sentence_tokens[index + 1:] in lcs):
            orig_indices.append(index + 1)
            susp_indices.append(index + 1)
        elif (original != suspect and original_sentence_tokens[index + 1:]
              in lcs and original_sentence_tokens[index + 1:] == -1):   # so this and prev elif - check and think what to do...
            pass


    all_indices.append(tuple(orig_indices))
    all_indices.append(tuple(susp_indices))
    indices = tuple(all_indices)
    print(indices)
    return indices

find_diff_in_sentence(original_sentence_tokens, suspicious_sentence_tokens, lcs)



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

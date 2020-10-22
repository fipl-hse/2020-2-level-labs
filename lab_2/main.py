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
    if isinstance(text,str):
        if isinstance(text, str):
            lines = []
            new_text = text.split('\n')
            for i in new_text:
                new_line=tuple(tokenizer.tokenize(i))
                if new_line:
                    lines.append(new_line)
            return (tuple(lines))
    return ()

def create_zero_matrix(rows: int, columns: int) -> list:
    """
    Creates a matrix rows * columns where each element is zero
    :param rows: a number of rows
    :param columns: a number of columns
    :return: a matrix with 0s
    e.g. rows = 2, columns = 2
    --> [[0, 0], [0, 0]]
    """
    req=[isinstance (rows,int), isinstance(columns,int), not isinstance(rows,bool),
         not isinstance(columns,bool)]
    if all (req) and rows>0 and columns>0:
        matrix = [[0] * columns for i in range(rows)]
        return(matrix)
    return  []


def fill_lcs_matrix(first_sentence_tokens: tuple, second_sentence_tokens: tuple) -> list:
    """
    Fills a longest common subsequence matrix using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :return: a lcs matrix
    """
    if isinstance(first_sentence_tokens,tuple) and  isinstance(second_sentence_tokens,tuple) \
            and None not in first_sentence_tokens and None not in second_sentence_tokens\
            and len(first_sentence_tokens) and len(second_sentence_tokens):
        matrix=create_zero_matrix(len(first_sentence_tokens)+1,len(second_sentence_tokens)+1)
        for index_1, element_1 in enumerate(first_sentence_tokens,1):
            for index_2, element_2 in enumerate(second_sentence_tokens,1):
                if element_1==element_2:
                    matrix[index_1][index_2]=matrix[index_1-1][index_2-1]+1
                else:
                    matrix[index_1][index_2] = max(matrix[index_1 - 1][index_2 ], matrix[index_1 ][index_2 -1])
        for element in matrix:
            element.remove (element[0])
        matrix.remove(matrix [0])
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
    lcs_matrix = fill_lcs_matrix(first_sentence_tokens, second_sentence_tokens)
    if isinstance (plagiarism_threshold, float) and plagiarism_threshold>0 and plagiarism_threshold<=1 \
            and isinstance(first_sentence_tokens,tuple) and isinstance(second_sentence_tokens,tuple) \
            and None not in first_sentence_tokens and None not in second_sentence_tokens :
        if not first_sentence_tokens or not second_sentence_tokens or len(second_sentence_tokens) < plagiarism_threshold:
            return 0
        length = lcs_matrix[-1][-1]
        return length
    return -1


def find_lcs(first_sentence_tokens: tuple, second_sentence_tokens: tuple, lcs_matrix: list) -> tuple:
    """
    Finds the longest common subsequence itself using the Needleman–Wunsch algorithm
    :param first_sentence_tokens: a tuple of tokens
    :param second_sentence_tokens: a tuple of tokens
    :param lcs_matrix: a filled lcs matrix
    :return: the longest common subsequence
    """
    if not isinstance(first_sentence_tokens, tuple) or not isinstance(second_sentence_tokens, tuple) \
            or  not first_sentence_tokens or  not second_sentence_tokens or \
             not all(isinstance(i, str) for i in first_sentence_tokens) or  not all(isinstance(i, str) for i in second_sentence_tokens) :
        return ()
    if not isinstance(lcs_matrix, list) or  not lcs_matrix or  not all(isinstance(i,list)for i in lcs_matrix )\
            or  not ( lcs_matrix[0][0]==0 or  lcs_matrix[0][0]==1) \
                      or not len(lcs_matrix)==len(first_sentence_tokens) or not len(lcs_matrix[0])==len(second_sentence_tokens):
        return ()
    lcs = []
    for index_1, element_1 in reversed(list(enumerate(first_sentence_tokens))):
        for index_2, element_2 in reversed(list(enumerate(second_sentence_tokens))):
            if element_1 == element_2:
                lcs.append(element_1)
                index_1-=1
                index_2-=2
            elif lcs_matrix[index_1 - 1][index_2] > lcs_matrix[index_1][index_2 - 1]:
                index_1-=1
            else:
                index_2-=1
    return tuple(lcs [::-1])


def calculate_plagiarism_score(lcs_length: int, suspicious_sentence_tokens: tuple) -> float:
    """
    Calculates the plagiarism score
    The score is the lcs length divided by the number of tokens in a suspicious sentence
    :param lcs_length: a length of the longest common subsequence
    :param suspicious_sentence_tokens: a tuple of tokens
    :return: a score from 0 to 1, where 0 means no plagiarism, 1 – the texts are the same
    """
    if not isinstance(lcs_length,int) or not isinstance(suspicious_sentence_tokens,tuple)\
            or lcs_length<0 or not all(isinstance (i,str) for i in suspicious_sentence_tokens) \
             or  isinstance(lcs_length,bool)  or (lcs_length>len(suspicious_sentence_tokens) and suspicious_sentence_tokens):
        return -1
    elif not suspicious_sentence_tokens :
        return 0.0
    score=lcs_length/len(suspicious_sentence_tokens)
    return score

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
    if  not isinstance(original_text_tokens,tuple) or not isinstance(suspicious_text_tokens,tuple)\
    or not isinstance(plagiarism_threshold,float)  or not 0<=plagiarism_threshold<=1\
    or not original_text_tokens or not suspicious_text_tokens \
    or not  all(isinstance(i, tuple) for i in original_text_tokens)\
    or not all(isinstance(i, tuple) for i in suspicious_text_tokens)\
    or not all(isinstance(i,str) for element in original_text_tokens for i in element)\
    or not  all(isinstance(i,str) for element in suspicious_text_tokens for i in element):
        return -1.0
    if len(original_text_tokens)<len(suspicious_text_tokens):
        original_text_tokens+=((),)*(len(suspicious_text_tokens)-len(original_text_tokens))
    elif len(original_text_tokens)>len(suspicious_text_tokens):
        original_text_tokens[:(len(suspicious_text_tokens))]
    sent_plagiarism=0
    for i in range(len(suspicious_text_tokens)):
        lcs_length_sent= find_lcs_length(original_text_tokens[i],suspicious_text_tokens[i],plagiarism_threshold)
        calc_plag_sent=calculate_plagiarism_score(lcs_length_sent,suspicious_text_tokens[i])
        sent_plagiarism+=calc_plag_sent
    text_plagiarism=sent_plagiarism/len(suspicious_text_tokens)
    return text_plagiarism



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

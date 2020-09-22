import re
import os


def tokenize(text: str) -> list:
    try:
        output = re.sub(r'[^a-z0-9\s]+', '', text.lower()).split()
    except AttributeError:
        output = []
    return output


def remove_stop_words(tokens: list, stop_words: list) -> list:
    if isinstance(tokens, list):    # check tokens
        if isinstance(stop_words, list):    # check stop-words
            output = [word for word in tokens if word not in stop_words]
        else:
            output = tokens
    else:
        output = []
    return output


def calculate_frequencies(tokens: list) -> dict:
    freqs = {}
    check = isinstance(tokens, list) and len(tokens) > 0
    if check and isinstance(tokens[0], str):    # check tokens
        for word in set(tokens):
            freqs[word] = tokens.count(word)
        freqs = dict(sorted(freqs.items(), key=lambda x: x[1], reverse=True))
    else:
        None
    return freqs


def get_top_n_words(freq_dict: dict, top_n: int) -> list:
    if isinstance(freq_dict, dict) and isinstance(top_n, int):
        freq_dict = sorted(freq_dict, key=freq_dict.get, reverse=True)
        output = freq_dict[:top_n]
    else:
        output = []
    return output


def get_concordance(tokens: list,
                    word: str,
                    left_context_size: int,
                    right_context_size: int) -> list:
    if isinstance(tokens, list) and word in tokens:    # check tokens & word
        check_l = not isinstance(left_context_size, bool) and isinstance(left_context_size, int) and left_context_size > 0
        check_r = not  isinstance(right_context_size, bool) and isinstance(right_context_size, int) and right_context_size > 0
        conc = []
        idx = [i for i, x in enumerate(tokens) if x == word]
        if check_l and check_r:
            for i in idx:
                conc.append(tokens[i-left_context_size:i+right_context_size+1])
        elif not check_l and check_r:
            for i in idx:
                conc.append(tokens[i:i+right_context_size+1])
        elif check_l and not check_r:
            for i in idx:
                conc.append(tokens[i-left_context_size:i+1])
        output = conc
    else:
        output = []
    return output


def get_adjacent_words(tokens: list,
                       word: str,
                       left_n: int,
                       right_n: int) -> list:
    conc = get_concordance(tokens, word, left_n, right_n)
    if left_n == 0:
        output = [[elem[-1]] for elem in conc]
    elif right_n == 0:
        output = [[elem[0]] for elem in conc]
    else:
        output = [[elem[0], elem[-1]] for elem in conc]
    return output


def read_from_file(path_to_file: str) -> str:
    with open(path_to_file, 'r', encoding='utf-8') as file:
        data = file.read()
    output = data
    return output


def write_to_file(path_to_file: str, content: list):
    with open(os.path.join(path_to_file, 'report.txt'),
              'w', encoding='utf-8') as file:
        file.write('\n'.join([' '.join(k) for k in content]))


def sort_concordance(tokens: list,
                     word: str,
                     left_context_size: int,
                     right_context_size: int,
                     left_sort: bool) -> list:
    output = []
    if isinstance(left_sort, bool):
        conc = get_concordance(tokens,
                               word,
                               left_context_size,
                               right_context_size)
        try:
            if left_context_size > 0 or right_context_size > 0:
                if left_sort and left_context_size > 0:
                    output = sorted(conc, key=lambda x: x[0])
                elif not left_sort and right_context_size > 0:
                    try:
                        rcs = right_context_size
                        output = sorted(conc, key=lambda x: x[-rcs])
                    except IndexError:
                        rcs = len(tokens) - tokens.index(word) - 1
                        output = sorted(conc, key=lambda x: x[-rcs])
        except TypeError:
            output = []
    else:
        output = []
    return output

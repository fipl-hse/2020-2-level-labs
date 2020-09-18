import re


def tokenize(text: str) -> list:
    if type(text) == str and text:
        prepared_text = re.sub('[^a-zA-Z ]', '', text).lower()
        return prepared_text.split()

    return []


def remove_stop_words(tokens: list, stop_words: list) -> list:
    if type(tokens) == list and tokens:
        if type(stop_words) == list and stop_words:
            clean_tokens = tokens[:]
            for word in tokens:
                if word in stop_words:
                    clean_tokens.remove(word)
            return clean_tokens

        else:
            return tokens

    else:
        return []


'''Ключ - токен, значение - число (частота). Функция должна возвращать объект типа dict.

Если на вход подаются некорректные токены, возвращается пустой словарь.'''


def calculate_frequencies(tokens: list) -> dict:
    if type(tokens) == list and tokens:
        return {word: tokens.count(word) for word in tokens}

    return {}


def get_top_n_words(freq_dict: dict, top_n: int) -> list:  # если несколько слов с одной частотой?
    if type(freq_dict) == dict and type(top_n) == int and freq_dict and top_n:
        list_items = freq_dict.items()
        values_dict = {}

        for i in list_items:
            if i[1] in values_dict.keys():
                values_dict[i[1]].append(i[0])
            else:
                values_dict[int(i[1])] = [i[0]]

        top_n_list = list(values_dict.keys())
        top_n_list.sort()

        top_values = [values_dict[top_n_list[-i]] for i in range(1, top_n + 1) if len(values_dict) >= top_n]

        return top_values


'''Функция должна возвращать список употреблений данного слова в тексте. При этом на количество слов в левом и в правом контексте накладываются ограничения.

Если на вход подаются некорректные токены или слово, возвращается пустой список.'''


def get_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int) -> list:
    tokens_copy = tokens.copy()
    inds = []

    while word in tokens_copy:
        inds.append(tokens_copy.index(word))
        tokens_copy.remove(word)

    if left_context_size > 0 and right_context_size > 0:
        return [tokens[i - left_context_size:i + right_context_size + 1] for i in inds]
    elif left_context_size > 0:
        return [tokens[i - left_context_size:i + 1] for i in inds]
    elif right_context_size > 0:
        return [tokens[i:i + right_context_size + 1] for i in inds]
    else:
        return []


def get_adjacent_words(tokens: list, word: str, left_n: int, right_n: int) -> list:
    pass


def write_to_file(path_to_file: str, content: list):
    pass


def sort_concordance(tokens: list, word: str, left_context_size: int, right_context_size: int, left_sort: bool) -> list:
    pass


data = 'The United States does not celebrate national holidays. But Congress has designated 10 "legal public ' \
       'holidays," ' \
       'during which most federal institutions are closed and most federal employees have days off work.' \
       'Since 1971, a number of the holidays have been fixed on Mondays, so as to celebrate workers a long holiday ' \
       'weekend.' \
       'Among most favorite American holidays are the following ones'

tokens_list = tokenize(data)

'''with open('stop_words.txt', 'r') as f:
    stop_list = f.read().split('\n')'''

stop_list = ['and', 'it', 'is']

prepared_tokens = remove_stop_words(tokens_list, stop_list)

freq_dict = calculate_frequencies(prepared_tokens)
print(get_top_n_words(freq_dict, 1))
print(get_concordance(prepared_tokens, 'celebrate', 2, 3))

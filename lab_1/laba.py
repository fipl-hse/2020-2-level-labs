import re


def tokenize(text):
    if type(text) != str:
        return []
    text = text.lower()
    text = re.sub(r'[^A-Za-z 0-9]', '', text)
    return text.split()


# print(tokenize("lfjh't jcfngjn'tyern,  ndgkjnm: ng-fjgn ab eakrgn75/ 348hgjengn erngh44"))
# print(tokenize('HJJBghvhgcJHughb &^%%%hvgv yg  TFYTFYVhf*( gff576^#$#&# hbgyg((878hbgv'))
# print(tokenize(''))
# print(tokenize(987876))

def remove_stop_words(tokens, stop_words):
    if type(tokens) != list:
        return []
    elif type(stop_words) != list:
        return tokens
    tokens_required = []
    for tok in tokens:
        if tok not in stop_words:
            tokens_required.append(tok)
    return tokens_required


# b = tokenize('always be a powerful girl sis it is essential')
# print(b)
# a = remove_stop_words(b, ['always', 'it'])
# print(a)

def calculate_frequencies(tokens):
    if type(tokens) != list:
        return {}
    freq_dict = {}
    for tok in tokens:
        if tok in freq_dict.keys():
            freq_dict[tok] += 1
        else:
            freq_dict[tok] = 1
    return freq_dict


n = calculate_frequencies(['all', 'g', 'a', 'greg', 'g', 'always', 'all', 'g', 'a', 'tyr', 'a', 'g'])


def get_top_n_words(freq_dict, top_n):
    if (type(freq_dict) != dict) or (type(top_n) != int):
        return []
    list_dict_items = list(freq_dict.items())
    # print(list_dict_items)
    list_dict_items.sort(key=lambda k_v: k_v[1], reverse=True)
    # вызываем анонимную ф-ю чтобы сортировка была по второму элементу кортежа (по численности)
    # print(list_dict_items)
    top_words = []
    if top_n > len(list_dict_items):
        return []
    else:
        for i in range(top_n):
            top_words.append(list_dict_items[i][0])
        return top_words


top = get_top_n_words(n, 5)


def get_concordance(tokens, word, left_context_size, right_context_size):
    concordance = []
    if (type(tokens) != list) or (type(word) != str):
        return []
    elif word not in tokens:
        return []
    elif (type(left_context_size) != int) and (type(right_context_size) != int):
        return []
    for ind, w in enumerate(tokens):
        if w == word:
            if (type(left_context_size) != int) or (left_context_size < 1):
                concordance += [tokens[ind:(ind + right_context_size + 1)]]
            elif (type(right_context_size) != int) or (right_context_size < 1):
                concordance += [tokens[(ind - left_context_size):(ind + 1)]]
            elif ind < left_context_size:
                concordance += [tokens[:(ind + right_context_size + 1)]]
            else:
                left_cont = ind - left_context_size
                right_cont = ind + right_context_size + 1
                concordance += [tokens[left_cont:right_cont]]
    return concordance


# erg = ['yesterday', 'the', 'weather', 'was', 'sunny', 'and', 'windy', 'today', 'it', 'is', 'sunny', 'and', 'windy', 'too']
# print(get_concordance(erg, 'sunny', 3, 1))

def get_adjacent_words(tokens, word, left_n, right_n):
    if (type(tokens) != list) or (type(word) != str):
        return []
    elif word not in tokens:
        return []
    elif (type(left_n) != int) and (type(right_n) != int):
        return []
    list_concordance = get_concordance(tokens, word, left_n, right_n)
    adjacent_words = []
    for cont_list in list_concordance:
        for ind, w in enumerate(cont_list):
            if w == word:
                if (type(left_n) != int) or (left_n < 0):
                    adjacent_words += [[cont_list[ind + right_n]]]
                elif (type(right_n) != int) or (right_n < 0):
                    adjacent_words += [[cont_list[ind - left_n]]]
                elif len(cont_list[:ind]) < left_n:
                    adjacent_words += [[cont_list[0], cont_list[ind + right_n]]]
                elif len(cont_list[(ind + 1):]) < right_n:
                    adjacent_words += [[cont_list[ind - left_n], cont_list[-1]]]
                else:
                    adjacent_words += [[cont_list[ind - left_n], cont_list[ind + right_n]]]
    return adjacent_words


# erg = ['yesterday', 'the', 'weather', 'was', 'sunny', 'and', 'windy', 'today', 'it', 'is', 'sunny', 'and', 'windy', 'too']
# print(get_adjacent_words(erg, 'sunny', 3, 1))


def write_to_file(path_to_file, content):
    context_list = []
    for word_list in content:
        s = ' '.join(word_list)
        context_list.append(s)
    context_str = '\n'.join(context_list)
    name_file = path_to_file + 'report.txt'
    with open(name_file, 'w') as f:
        f.write(context_str)


# hr = [['the', 'weather', 'was', 'sunny', 'and'], ['today', 'it', 'is', 'sunny', 'and']]
# write_to_file(r'C:\Users\79121\Documents\универ\\', hr)


def sort_concordance(tokens, word, left_context_size, right_context_size, left_sort):
    if type(left_sort) != bool:
        return []
    list_concordance = get_concordance(tokens, word, left_context_size, right_context_size)
    if left_sort:
        list_concordance.sort(key=lambda w: w[0])
    else:
        index_word = left_context_size + 1  # считаю индекс правого слова для сортировки
        list_concordance.sort(key=lambda w: w[index_word])
    return list_concordance


# erg = ['yesterday', 'the', 'weather', 'was', 'sunny', 'and', 'windy', 'today', 'it', 'is', 'sunny', 'and', 'windy', 'too']
# print(sort_concordance(erg, 'sunny', 1, 1, True))

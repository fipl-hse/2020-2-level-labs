"""
Tokenizer out of lab_1 for usage in lab_2
"""


def tokenize(text: str) -> tuple:

    print()
    signs = ".,;:%#№@$&*=+`\"\'.!?—(){}[]-><|"
    clean_text = ''

    for i in range(len(text)):  # цикл по длине строки
        if text[i] in signs:  # если в введенной строке нашли знак препинания
            clean_text += ''
        else:
            clean_text += text[i]

    clean_text = clean_text.lower().split('\n')
    # print(clean_text)
    tuple_text = tuple(tuple(elem.split(' ')) for elem in clean_text)

#   new_text = tuple(new_text) тюплим список - получаем элементы списка, если тюплим строку, то получаем набор символов

    return tuple_text

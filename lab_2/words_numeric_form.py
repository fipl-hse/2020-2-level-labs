"""
Create a dictionary with words and corresponding numbers
"""
import re
import pickle


def make_words_numeric(path_to_file):
    words_dict = {}
    word_number = 0
    with open(path_to_file, encoding='utf-8') as data_file:
        for line in data_file.readlines():
            tokenized_line = re.sub('[^a-z \n]', '', line.lower()).split()
            for token in tokenized_line:
                if token not in words_dict:
                    words_dict[token] = word_number
                    word_number += 1
    return words_dict


words_numeric_text = make_words_numeric('lab_2/data.txt')
words_numeric_second_text = make_words_numeric('lab_2/data_2.txt')
words_numeric_text.update(words_numeric_second_text)

file = open('lab_2/numeric_words.csv', 'wb')
pickle.dump(words_numeric_text, file)

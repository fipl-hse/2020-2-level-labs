import csv
import re


def make_vocabulary(path_to_file, vocabulary=dict(), i=0):
    with open(path_to_file, 'r', encoding='utf-8') as file:
        for line in file:
            tokens = re.sub('[^a-z \n]', '', line.lower()).split()
            for key in tokens:
                if key not in vocabulary:
                    vocabulary[key] = i
                    i += 1

                    with open('vocabulary.csv', 'a', encoding='utf-8') as f:
                        f.write(f'{key}, {vocabulary[key]}\n')


make_vocabulary('data.txt')
make_vocabulary('data_2.txt')

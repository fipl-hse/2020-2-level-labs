import csv
from tokenizer import tokenize


def make_vocabulary(path_to_file, vocabulary=dict(), i=0):
    for line in open(path_to_file, 'r', encoding='utf-8'):
        tokens = tokenize(line.lower())
        for key in tokens:
            if key not in vocabulary:
                vocabulary[key] = i
                i = len(vocabulary)

                with open('vocabulary.csv', 'a', encoding='utf-8') as f:
                    f.write(f'{key}, {vocabulary[key]}\n')


make_vocabulary('data.txt')
make_vocabulary('data_2.txt')

import pickle
import re

vocabulary = {'_i': 0}

def make_vocabulary(path_to_file):
    with open(path_to_file, 'r', encoding='utf-8') as file:
        for line in file:
            tokens = re.sub('[^a-z \n]', '', line.lower()).split()
            for key in tokens:
                if key not in vocabulary:
                    vocabulary[key] = vocabulary['_i']
                    vocabulary['_i'] += 1
    return vocabulary

vocabulary = make_vocabulary('data.txt')
vocabulary = make_vocabulary('data_2.txt')

with open('vocabulary.pickle', 'wb') as file:
    pickle.dump(vocabulary, file)

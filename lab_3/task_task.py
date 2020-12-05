from lab_3.main import *

a = LetterStorage()
corpus = tokenize_by_sentence("I am gay")
a.update(corpus)
corpus = encode_corpus(a, corpus)
# print(a.storage)
# a.storage = {v:k for k, v in a.storage.items()}
print(a.storage)


def encode_corpus1(storage: LetterStorage, corpus: tuple) -> tuple:
    result = []
    my_id = ""
    for sentence in corpus:
        result_sentence = []
        for word in sentence:
            result_word = []
            for letter in word:
                for k, v in a.storage.items():
                    if v == letter:
                        my_id = k
                result_word.append(my_id)
            result_sentence.append(tuple(result_word))
        result.append(tuple(result_sentence))
    return tuple(result)


print(encode_corpus1(a, corpus))

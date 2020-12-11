from lab_4 import main

if __name__ == '__main__':
    text = 'I have a cat.\nHis name is Bruno'
    corpus = main.tokenize_by_sentence(text)
    print(corpus)

    storage = main.WordStorage()
    storage.update(corpus)
    print(storage.storage)

    encoded = main.encode_text(storage, corpus)
    print(encoded)

    RESULT = encoded
    assert RESULT == (1, 2, 3, 4, 5, 6, 7, 8, 9, 5), 'Not working'



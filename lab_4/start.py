from main import tokenize_by_sentence
from main import WordStorage
from main import encode_text

if __name__ == '__main__':
    text = 'Somebody once told me a secret. \n Somebody ones told the world is gonna roll me'
    corpus = tokenize_by_sentence(text)
    print(corpus)

    word_storage = WordStorage()
    word_storage.update(corpus)
    print(word_storage)

    encoded_text = encode_text(word_storage, corpus)
    print(encode_text)

    RESULT = "('somebody', 'once', 'told', 'me', 'a', 'secret', '<END>', 'somebody', 'ones', 'told', 'the', 'world', 'is', 'gonna', 'roll', 'me', '<END>')"
    print(RESULT)
    assert RESULT == "('somebody', 'once', 'told', 'me', 'a', 'secret', '<END>', 'somebody', 'ones', 'told', 'the', 'world', 'is', 'gonna', 'roll', 'me', '<END>')", 'Something went wrong'
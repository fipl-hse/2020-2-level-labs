from lab_4.main import tokenize_by_sentence
from lab_4.main import WordStorage
from lab_4.main import encode_text

if __name__ == '__main__':
    text = 'She is happy. He is happy.'
    corpus = tokenize_by_sentence(text)

    word_storage = WordStorage()
    word_storage.update(corpus)

    encoded_text = encode_text(word_storage, corpus)

    RESULT = "('she', 'is', 'happy', '<END>', 'he', 'is', 'happy', '<END>')"
    print(RESULT)
    assert RESULT == "('she', 'is', 'happy', '<END>', 'he', 'is', 'happy', '<END>')", 'Something went wrong'
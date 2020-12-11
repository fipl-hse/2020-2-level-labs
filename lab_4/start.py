from lab_4.main import tokenize_by_sentence
from lab_4.main import WordStorage
from lab_4.main import encode_text

if __name__ == '__main__':
    text = 'His name is leon. He is happy.'
    corpus = tokenize_by_sentence(text)

    word_storage = WordStorage()
    word_storage.update(corpus)

    encoded_text = encode_text(word_storage, corpus)

    RESULT = "('he','is', 'leon' '<END>', 'he', 'is', 'happy', '<END>')"
    print(RESULT)
    assert RESULT == "('he','is', 'leon' '<END>', 'he', 'is', 'happy', '<END>')", 'Something went wrong'

from lab_4.main import WordStorage, NGramTrie, NGramTextGenerator
from lab_4.main import tokenize_by_sentence, encode_text

if __name__ == '__main__':
    text = 'I have a cat. His name is Bruno. I have a dog. Her name is Beth. '
    text_tokenized = tokenize_by_sentence(text)

    word_storage = WordStorage()
    word_storage.update(text_tokenized)

    encoded = encode_text(word_storage, text_tokenized)

    trie = NGramTrie(2, encoded)
    context = (word_storage.get_id('is'),)
    generator = NGramTextGenerator(word_storage, trie)

    RESULT = generator.generate_text(context, 4)

    print(RESULT)

    assert RESULT, "Not working"
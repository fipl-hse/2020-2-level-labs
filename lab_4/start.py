from lab_4.ngrams.ngram_trie import NGramTrie
from lab_4.main import tokenize_by_sentence
from lab_4.main import WordStorage
from lab_4.main import encode_text
from lab_4.main import NGramTextGenerator

if __name__ == '__main__':
    text = "This is a dog. It likes running. This is a cat. It likes sleeping. Everyone likes sleeping too."
    text_in_tokens = tokenize_by_sentence(text)

    word_storage = WordStorage()
    word_storage.update(text_in_tokens)

    encoded_text = encode_text(word_storage, text_in_tokens)

    n_gram_trie = NGramTrie(2, encoded_text)
    context = (word_storage.get_id('likes'),)
    text_generator = NGramTextGenerator(word_storage, n_gram_trie)

    RESULT = text_generator.generate_text(context, 4)

    print(RESULT)

    assert RESULT, "Someting went worng.."
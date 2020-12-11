"""
Generator of the text starter
"""

from lab_4.main import tokenize_by_sentence
from lab_4.main import WordStorage
from lab_4.ngrams.ngram_trie import NGramTrie
from lab_4.main import encode_text
from lab_4.main import NGramTextGenerator

if __name__ == '__main__':

    text = tokenize_by_sentence("""Hi everyone! Nice to meet you again. What are you doing in my laboratory work?
                                    You are very nice person, do you know it? To be honest, I can't stand programming.
                                    But it doesn't depend on you! It's my personal problem and I don't know how to
                                    solve it... It doesn't matter right now""")

    word_storage = WordStorage()
    word_storage.update(text)

    encoded_text = encode_text(word_storage, text)

    n_gram_trie = NGramTrie(3, encoded_text)

    generator_of_text = NGramTextGenerator(word_storage, n_gram_trie)
    context = word_storage.get_id('on'), word_storage.get_id('you')

    formed_ids = generator_of_text.generate_text(context, 1)
    formed_text = []

    for ids in formed_ids:
        word = word_storage.get_word(ids)
        if word != '<END>':
            formed_text.append(word)

    RESULT = ' '.join(formed_text)
    print(RESULT)
    assert RESULT == 'on you', ''

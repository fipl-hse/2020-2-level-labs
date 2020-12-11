"""
 Text generator
 """

from lab_4.ngrams.ngram_trie import NGramTrie
from lab_4.main import WordStorage
from lab_4.main import encode_text
from lab_4.main import NGramTextGenerator

if __name__ == '__main__':
    corpus = ('i', 'have', 'a', 'cat', '<END>',
                'his', 'name', 'is', 'bruno', '<END>',
                'i', 'have', 'a', 'dog', 'too', '<END>',
                'his', 'name', 'is', 'rex', '<END>',
                'her', 'name', 'is', 'rex', 'too', '<END>')

    word_storage = WordStorage()
    word_storage.update(corpus)

    encoded_text = encode_text(word_storage, corpus)

    n_gram_trie = NGramTrie(2, encoded_text)

    n_gram_text_generator = NGramTextGenerator(word_storage, n_gram_trie)

    context = (word_storage.get_id('Butter'), word_storage.get_id('unterheben'))

    text_generated = n_gram_text_generator.generate_text(context, 2)
    output_text = []
    for word_id in text_generated:
        word = word_storage.get_word(word_id)
            if word != '<END>':
                output_text.append(word)

    RESULT = ' '.join(output_text)
    print(RESULT)
    assert RESULT == ''
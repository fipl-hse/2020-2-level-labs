"""
Generator of something
"""

from lab_4.main import tokenize_by_sentence
from lab_4.main import WordStorage
from lab_4.ngrams.ngram_trie import NGramTrie
from lab_4.main import encode_text
from lab_4.main import NGramTextGenerator

if __name__ == '__main__':

    text = tokenize_by_sentence("""The idea is already raising interest in other cities. 
    Social workers will also be looking for other ways in which peer pressure can be used 
    to produce positive results, rather than negative ones. If more original ways can be found, t
    o make positive use of peer pressure, levels of crime and other social problems among teenagers and young will fall.
    Some people also say that a similar""")

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
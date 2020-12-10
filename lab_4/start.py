"""
Text generator
"""

from lab_4.ngrams.ngram_trie import NGramTrie
from lab_4.main import tokenize_by_sentence
from lab_4.main import WordStorage, LikelihoodBasedTextGenerator
from lab_4.main import encode_text, decode_text
from lab_4.main import NGramTextGenerator


if __name__ == '__main__':
    TEXT = 'I have a cat. His name is Bruno. I have a dog too. His name is Rex. Her name is Rex too.'
    tokenized_text = tokenize_by_sentence(TEXT)

    word_storage = WordStorage()
    word_storage.update(tokenized_text)

    encoded = encode_text(word_storage, tokenized_text)

    trie = NGramTrie(3, encoded)
    context = (word_storage.get_id('name'), word_storage.get_id('is'), )

    generator = NGramTextGenerator(word_storage, trie)
    generated_text = generator.generate_text(context, 2)

    gen_likelihood = LikelihoodBasedTextGenerator(word_storage, trie)
    gen_text = gen_likelihood.generate_text(context, 2)
    decoded_text = decode_text(word_storage, gen_text)

    RESULT = decoded_text

    assert RESULT == ('Name is rex', 'Her name is rex'), "Not working"

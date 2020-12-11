"""
 Text generator
 """
import main
from ngrams.ngram_trie import NGramTrie

if __name__ == '__main__':
    text = 'I want to pass exams. I do not want study morphology'
    corpus = main.tokenize_by_sentence(text)

    word_storage = main.WordStorage()
    word_storage.update(corpus)

    encoded_text = main.encode_text(word_storage, corpus)
    RESULT = encoded_text

    assert RESULT,''
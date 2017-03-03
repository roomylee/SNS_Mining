import numpy as np
import pandas as pd
from konlpy.tag import Twitter
import gensim
from sklearn.decomposition import PCA


def tokenize(doc):
    result = list()
    pos_tagger = Twitter()
    for s in pos_tagger.pos(doc, norm=True, stem=True):
        if s[1] in ['Noun', 'Verb', 'Adjective', 'Adverb']:
            result.append(s[0])
    return result


def make_model():
    df = pd.read_csv('tweet.csv')

    train_docs = list()
    for sentence in df['Contents']:
        try:
            train_docs.append(tokenize(sentence))
        except Exception as e:
            print(e)
            continue

    model = gensim.models.Word2Vec(train_docs)

    model.save('wv.model')

def vectorize(vocab):
    model = gensim.models.Word2Vec.load('wv.model')
    result = list()
    for word in vocab:
        result.append(model[word[0]])
    return result


def pca_projection(word2vec):
    pca = PCA(n_components=2)

    pca.fit(word2vec)
    projected_vec = pca.transform(word2vec)

    result = list()
    for vec in projected_vec:
        result.append([format(vec[0], '.1f'), format(vec[1], '.1f')])

    return result


if __name__ == '__main__':
    make_model()
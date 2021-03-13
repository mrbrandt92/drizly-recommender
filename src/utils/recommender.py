import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import wordnet as wn
import re
import numpy as np


def tfidf_vec(cats_df):
    vocabulary = set()
    for doc in cats_df.combined_cats:
        vocabulary.update(doc.split(' '))

    vocabulary = list(vocabulary)

    vectorizer = TfidfVectorizer(stop_words='english', vocabulary=vocabulary)
    vectorizer.fit(cats_df.combined_cats)

    tfidf_tran = vectorizer.transform(cats_df.combined_cats)

    return vocabulary, vectorizer, tfidf_tran


def transform(data):
    file_clean_k =pd.DataFrame()

    for index,entry in enumerate(data):
        Final_words = []
        for word, tag in pos_tag(entry):
            if len(word)>1 and word not in stopwords.words('english') and word.isalpha():
                Final_words.append(word)
                file_clean_k.loc[index,'Keyword_final'] = str(Final_words)
                file_clean_k=file_clean_k.replace(to_replace ="\[.", value = '', regex = True)
                file_clean_k=file_clean_k.replace(to_replace ="'", value = '', regex = True)
                file_clean_k=file_clean_k.replace(to_replace =" ", value = '', regex = True)
                file_clean_k=file_clean_k.replace(to_replace ='\]', value = '', regex = True)
    return file_clean_k


def gen_vector_T(cats_df,tokens):
    vocabulary, vectorizer, _ = tfidf_vec(cats_df)
    Q = np.zeros((len(vocabulary)))
    x = vectorizer.transform(tokens)
    for token in tokens[0].split(','):
        try:
            ind = vocabulary.index(token)
            Q[ind] = x[0, vectorizer.vocabulary_[token]]
        except Exception as e:
            print(e)

    return Q


def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))

    return cos_sim


def cosine_similarity_T(cats_df, user_row_df, k=4):
    preprocessed_query = user_row_df.combined_cats.to_string()
    tokens = word_tokenize(preprocessed_query)
    q_df = pd.DataFrame(columns=['q_clean'])
    q_df.loc[0,'q_clean'] = tokens
    q_df['q_clean'] = transform(q_df.q_clean)
    print(q_df.q_clean)
    d_cosines = []

    query_vector = gen_vector_T(cats_df,q_df['q_clean'])
    _, _, tfidf_tran = tfidf_vec(cats_df)
    for d in tfidf_tran.A:
        d_cosines.append(cosine_sim(query_vector, d))

    out = np.array(d_cosines).argsort()[-k:][::-1]
    d_cosines.sort()
    a = pd.DataFrame()
    for i,index in enumerate(out):
        a.loc[i,'catalog_item_name'] = cats_df['catalog_item_name'][index]
        a.loc[i, 'catalog_item_id'] = cats_df['catalog_item_id'][index]
    for j,simScore in enumerate(d_cosines[-k:][::-1]):
        a.loc[j,'score'] = simScore

    a['user_id_hash'] = user_row_df.user_id_hash.values[0]
    print(a)
    rec_dict = a.groupby('user_id_hash')[['catalog_item_id','catalog_item_name', 'score']]\
        .apply(lambda x: x.set_index('catalog_item_id').to_dict(orient='index'))\
        .to_dict()

    print(rec_dict)
    return rec_dict


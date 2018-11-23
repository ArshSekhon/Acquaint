import os
from time import time
import argparse
import pandas as pd
import multiprocessing
from time import time
import numpy as np
from collections import namedtuple
import gensim as gs
import os
import sys
import warnings
from random import shuffle
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Type
import matplotlib.pyplot as plt
import logging
from ast import literal_eval
import gensim.models.keyedvectors as word2vec

import pandas as pd
import nltk
import sys, codecs
import os
from time import time
import argparse
import pandas as pd
import multiprocessing
from time import time
import numpy as np
from collections import namedtuple
import gensim as gs
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import os
import sys
import warnings
from random import shuffle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from gensim.similarities import Similarity
from gensim.matutils import cossim
from typing import Dict, List, Type
import matplotlib.pyplot as plt
import logging
from ast import literal_eval
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import gensim
from gensim import corpora, models
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup

def predict_tags(input_id):
    
    #print(os.path.join(os.getcwd(), 'data', 'excel_files','mentors.csv'))
    df_peers = pd.read_csv(os.path.join(os.getcwd(),'server','data', 'excel_files','mentors.csv'))
    df_peers = df_peers[['id','Name','Expertise', 'Interest']]
    int = df_peers['Interest']
    exp = df_peers['Expertise']
    list_of_interestrs = []
    list_of_expertises = []
    list_of_interestrs_vector = []
    list_of_expertises_vector = []

    model = gs.models.KeyedVectors.load_word2vec_format(os.path.join(os.getcwd(),'server','models', 'word2vec_models','GoogleNews-vectors-negative300.bin'), limit=500000, binary=True)
    for i in range(len(int)):
        tags_int = str(int[i]).strip().split(',')
        tags_exp = str(exp[i]).strip().split(',')
        list_of_interestrs.append(tags_int)
        list_of_expertises.append(tags_exp)

    df_peers['expertise_list'] = list_of_expertises
    df_peers['interest_list'] = list_of_interestrs

    my_expertise = list_of_expertises[input_id]
    my_interests = list_of_interestrs[input_id]

    most_similar = []
    for index, other in enumerate(list_of_interestrs):
        if(index == input_id):
            most_similar.append(0)
            continue
        max = 0
        for other_interest in other:
            for interest in my_interests:
                if(len(other_interest.split())>1 or len(interest.split())>1):
                    #print('comparing ' + interest + ' with ' + other_interest)
                    temp_list_int_other = []
                    for other_interest_part in other_interest.split():
                        temp_list_int_other.append(model[other_interest_part])
                    avg_int_other = np.mean(temp_list_int_other)

                    temp_list_int = []
                    for interest_part in interest.split():
                        temp_list_int.append(model[interest_part])
                    avg_int = np.mean(temp_list_int)
                    sim = np.dot(avg_int, avg_int_other)
                    if (sim > max):
                        max = sim
                    continue
                #print('comparing '+interest+' with '+other_interest)
                sim = model.similarity(interest.strip(), other_interest.strip())
                if (sim > max):
                    max = sim
        most_similar.append(max)
    df_peers['similarity'] = most_similar


    most_similar_exp = []
    for index, other in enumerate(list_of_expertises):
        if (index == input_id):
            most_similar_exp.append(0)
            continue
        max = 0
        for other_expertises in other:
            for expertises in my_expertise:
                if (len(other_expertises.split()) > 1 or len(expertises.split()) > 1):
                    #print('comparing ' + expertises + ' with ' + other_expertises)
                    temp_list_exp_other = []
                    for other_expertise_part in other_expertises.split():
                        temp_list_exp_other.append(model[other_expertise_part])
                    avg_exp_other = np.mean(temp_list_exp_other)

                    temp_list_exp = []
                    for expertises_part in expertises.split():
                        temp_list_exp.append(model[expertises_part])
                    avg_exp = np.mean(temp_list_exp)
                    sim = np.dot(avg_exp, avg_exp_other)
                    if (sim > max):
                        max = sim
                    continue
                #print('comparing ' + expertises + ' with ' + other_expertises)
                sim = model.similarity(expertises.strip(), other_expertises.strip())
                if (sim > max):
                    max = sim
        most_similar_exp.append(max)
    df_peers['exp_similarity'] = most_similar_exp
    #print(most_similar)
    #print(most_similar_exp)
    df_int=df_peers.sort_values(by='similarity', ascending = False)
    #print(df_int['Name'][:3])
    interest = df_int['Name'][:3].tolist()
    print(type(interest))
    df_exp=df_peers.sort_values(by='exp_similarity', ascending = False)
    #print(df_exp['Name'][:3])
    expertise = df_exp['Name'][:3].tolist()
    print(type(expertise))
    return ( interest, expertise)


def run_lda(query):

    tokenizer = RegexpTokenizer(r'\w+')
    nltk.download('stopwords')
    stop_words = stopwords.words('english')
    p_stemmer = PorterStemmer()


    text_list = []
    raw = query.lower()
    tokens = tokenizer.tokenize(raw)
    stopped_tokens = [i for i in tokens if not i in stop_words]
    texts = [p_stemmer.stem(i) for i in stopped_tokens]
    text_list.append(stopped_tokens)
    dictionary = corpora.Dictionary(text_list)
    corpus = [dictionary.doc2bow(text) for text in text_list]
    lda = None
    try:
        ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=1, id2word=dictionary, passes=20)
    except:
        lda = 'None'

    x = ldamodel.show_topics(num_topics=1, num_words=4, formatted=False)
    topics_words = [(tp[0], [wd[0] for wd in tp[1]]) for tp in x]

    wordlist = []
    for topic, words in topics_words:
        wordlist.append(words)
    #print(wordlist)

    df_peers = pd.read_csv(os.path.join(os.getcwd(),'server','data', 'excel_files','mentors.csv'))
    df_peers = df_peers[['id', 'Name', 'Expertise', 'Interest']]
    int = df_peers['Interest']
    exp = df_peers['Expertise']
    list_of_interestrs = []
    list_of_expertises = []
    list_of_interestrs_vector = []
    list_of_expertises_vector = []

    model = gs.models.KeyedVectors.load_word2vec_format(
        os.path.join(os.getcwd(), 'server', 'models', 'word2vec_models', 'GoogleNews-vectors-negative300.bin'), limit=500000,
        binary=True)
    for i in range(len(int)):
        tags_int = str(int[i]).strip().split(',')
        tags_exp = str(exp[i]).strip().split(',')
        list_of_interestrs.append(tags_int)
        list_of_expertises.append(tags_exp)

    df_peers['expertise_list'] = list_of_expertises
    df_peers['interest_list'] = list_of_interestrs

    my_expertise = words
    my_interests = words

    most_similar = []
    for index, other in enumerate(list_of_interestrs):
        max = 0
        for other_interest in other:
            for interest in my_interests:
                if (len(other_interest.split()) > 1 or len(interest.split()) > 1):
                    #print('comparing ' + interest + ' with ' + other_interest)
                    temp_list_int_other = []
                    for other_interest_part in other_interest.split():
                        temp_list_int_other.append(model[other_interest_part])
                    avg_int_other = np.mean(temp_list_int_other)

                    temp_list_int = []
                    for interest_part in interest.split():
                        temp_list_int.append(model[interest_part])
                    avg_int = np.mean(temp_list_int)
                    sim = np.dot(avg_int, avg_int_other)
                    if (sim > max):
                        max = sim
                    continue
                #print('comparing ' + interest + ' with ' + other_interest)
                sim = model.similarity(interest.strip(), other_interest.strip())
                if (sim > max):
                    max = sim
        most_similar.append(max)
    df_peers['similarity'] = most_similar

    most_similar_exp = []
    for index, other in enumerate(list_of_expertises):
        max = 0
        for other_expertises in other:
            for expertises in my_expertise:
                if (len(other_expertises.split()) > 1 or len(expertises.split()) > 1):
                    #print('comparing ' + expertises + ' with ' + other_expertises)
                    temp_list_exp_other = []
                    for other_expertise_part in other_expertises.split():
                        temp_list_exp_other.append(model[other_expertise_part])
                    avg_exp_other = np.mean(temp_list_exp_other)

                    temp_list_exp = []
                    for expertises_part in expertises.split():
                        temp_list_exp.append(model[expertises_part])
                    avg_exp = np.mean(temp_list_exp)
                    sim = np.dot(avg_exp, avg_exp_other)
                    if (sim > max):
                        max = sim
                    continue
                #print('comparing ' + expertises + ' with ' + other_expertises)
                sim = model.similarity(expertises.strip(), other_expertises.strip())
                if (sim > max):
                    max = sim
        most_similar_exp.append(max)
    df_peers['exp_similarity'] = most_similar_exp

    df_peers['exp_similarity'] = most_similar_exp
    #print(most_similar)
    #print(most_similar_exp)
    df_int = df_peers.sort_values(by='similarity', ascending=False)
    #print(df_int['Name'][:3])
    interest = df_int['Name'][:3].tolist()
    df_exp = df_peers.sort_values(by='exp_similarity', ascending=False)
    #print(df_exp['Name'][:3])
    expertise = df_exp['Name'][:3].tolist()
    print(">>>>",type(interest))
    return (interest, expertise)

def read_from_url(url):


    #url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
    html = urlopen(url).read()
    raw = BeautifulSoup(html).get_text()
    tokens = nltk.word_tokenize(raw)
    print(tokens)
    text = " ".join(tokens)
    run_lda(text)

if __name__ == "__main__":
     predict_tags(0)
     #run_lda("The foreign buyer’s tax – in all of its forms and under different governments – never caused strife among voters. It achieved a status that is seldom seem in a province as polarized politically as British Columbia, with NDP voters approving of the actions of Christy Clark in 2016 and BC Liberal voters thinking the current government’s changes were admissible in 2017.")
     #read_from_url("http://news.bbc.co.uk/2/hi/health/2284783.stm")
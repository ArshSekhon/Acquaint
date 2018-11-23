import sqlite3
import pandas as pd
import numpy as np
import gensim as gs
import os
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import gensim
from gensim import corpora, models
import nltk
from urllib.request import urlopen
from bs4 import BeautifulSoup

def calculate_pairwise_similarity(list_A, list_B, dictionary, model):
    similarity = 0
    max = 0
    for other_interest in list_A:
        for interest in list_B:
            if (len(other_interest.split()) > 1 or len(interest.split()) > 1):
                # print('comparing ' + interest + ' with ' + other_interest)
                temp_list_int_other = []
                for other_interest_part in other_interest.split():
                    if (other_interest_part in dictionary):
                        temp_list_int_other.append(model[other_interest_part])
                avg_int_other = np.mean(temp_list_int_other)

                temp_list_int = []
                for interest_part in interest.split():
                    if (interest_part in dictionary):
                        temp_list_int.append(model[interest_part])
                avg_int = np.mean(temp_list_int)
                sim = np.dot(avg_int, avg_int_other)
                if (sim > max):
                    max = sim
                continue
            elif (interest.strip() not in dictionary or other_interest.strip() not in dictionary):
                continue
            sim = model.similarity(interest.strip(), other_interest.strip())
            if (sim > max):
                max = sim
    return max

def get_list_of_similarities(one_d_list, two_d_list, dictionary, model, input_id = -1):
    most_similar = []
    for index, other in enumerate(two_d_list):
        if (index == input_id):
            most_similar.append(0)
            continue
        else:
            max = calculate_pairwise_similarity(other, one_d_list, dictionary, model)
            most_similar.append(max)
    return most_similar

def read_from_db():
    conn = sqlite3.connect('database.db')
    members = pd.read_sql_query("select * from members;", conn)
    ids, emails, names, inums = members['mid'], members['email'], members['name'], members['i_num']

    interest_list = []
    interest_level_list = []
    interests = pd.read_sql_query("select * from interest;", conn)
    print(interests)

    for i in range(len(names)):
        intrsts = []
        levels = []
        for index, row in interests.iterrows():
            if(row[0]==i):
                intrsts.append(row[1])
                levels.append(row[2])
        interest_list.append(intrsts)
        interest_level_list.append(levels)

    expertise_list = []
    expertise_level_list = []
    expertises = pd.read_sql_query("select * from expertise;", conn)

    for i in range(len(names)):
        exprts = []
        levels = []
        for index, row in expertises.iterrows():
            if (row[0] == i):
                exprts.append(row[1])
                levels.append(row[2])
        expertise_list.append(exprts)
        expertise_level_list.append(levels)

    conn.commit()
    conn.close()

    df_peers_dict = {
        'id': ids,
        'email': emails,
        'Name': names,
        'i_number': inums,
        'Expertise': expertise_list,
        'Expertise_level': expertise_level_list,
        'Interest': interest_list,
        'Interest_level': interest_level_list
    }

    df_peers = pd.DataFrame.from_dict(df_peers_dict)
    df_peers.to_csv('test.csv')
    return df_peers

def predict_tags(input_id):
    model = gs.models.KeyedVectors.load_word2vec_format(
        os.path.join(os.getcwd(), 'server', 'models', 'word2vec_models', 'GoogleNews-vectors-negative300.bin'),
        limit=500000, binary=True)
    dictionary = model.wv.vocab

    df_peers = read_from_db()
    df_peers = df_peers[['id','Name','Expertise', 'Interest']]
    list_of_interestrs = df_peers['Interest'].tolist()
    list_of_expertises = df_peers['Expertise'].tolist()

    df_peers['similarity'] = get_list_of_similarities(list_of_interestrs[input_id], list_of_interestrs, dictionary, model, input_id )
    df_peers['exp_similarity'] = get_list_of_similarities(list_of_expertises[input_id], list_of_expertises, dictionary, model, input_id )
    interest = df_peers.sort_values(by='similarity', ascending = False)['Name'][:3].tolist()
    expertise = df_peers.sort_values(by='exp_similarity', ascending = False)['Name'][:3].tolist()
    print(interest)
    print(expertise)
    return (interest, expertise)

def get_lda(query):
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
    return ldamodel

def update_or_create_entry(id, intrst):
    id = int(id)
    print('insert '+str(intrst)+' into interest where id = '+ str(id))
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM interest WHERE intrst_id = ? AND interest = ?', (id, intrst))
    exists = cur.fetchall()

    if not exists:
        print('if case')
        cur.execute("INSERT INTO interest (intrst_id, interest, level) VALUES (?,?,?)", (id, intrst, 1))
    else:
        print('else case')
        cur.execute('UPDATE interest SET level = level + 1 WHERE interest = ?', (intrst,))
    conn.commit()
    conn.close()

def is_technical(word):
    cur_path = os.getcwd()
    path_to_tags = None
    if 'server' in cur_path:
        path_to_tags = os.path.join(os.getcwd(),'data', 'excel_fles', 'tags.csv')
    else:
        path_to_tags = os.path.join(os.getcwd(), 'server', 'data', 'excel_files', 'tags.csv')
    df_tags = pd.read_csv(path_to_tags)
    tags = df_tags['TagName'].tolist()
    if word in tags:
        return True
    return False

def run_lda(query, id=-1, from_url = False):
    ldamodel = get_lda(query)
    x = ldamodel.show_topics(num_topics=1, num_words=3, formatted=False)
    topics_words = [(tp[0], [wd[0] for wd in tp[1]]) for tp in x]
    model = gs.models.KeyedVectors.load_word2vec_format(
        os.path.join(os.getcwd(), 'server', 'models', 'word2vec_models', 'GoogleNews-vectors-negative300.bin'),
        limit=500000, binary=True)
    dictionary = model.wv.vocab

    df_peers = read_from_db()
    df_peers = df_peers[['id', 'Name', 'Expertise', 'Interest']]
    list_of_interestrs = df_peers['Interest'].tolist()
    list_of_expertises = df_peers['Expertise'].tolist()

    wordlist = []
    for topic, words in topics_words:
        for word in words:
            if word in dictionary:
                wordlist.append(word)

    if(from_url == True):
        for word in wordlist:
            if is_technical(word):
                print(type(id))
                update_or_create_entry(id=id, intrst=word)

    df_peers['similarity'] = get_list_of_similarities(wordlist, list_of_interestrs, dictionary, model, id)
    df_peers['exp_similarity'] = get_list_of_similarities(wordlist, list_of_expertises, dictionary, model, id)
    interest = df_peers.sort_values(by='similarity', ascending=False)['Name'][:3].tolist()
    expertise = df_peers.sort_values(by='exp_similarity', ascending=False)['Name'][:3].tolist()
    print(interest)
    print(expertise)
    return (interest, expertise)

def inum_to_id(inum, df_peer):
    ids = df_peer['id']
    inums = df_peer['i_number']
    for i in range(len(inums)):
        if(inums[i] == inum):
            return ids[i]
    return -1




def read_from_url(inum, url):
    #url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
    df_peer = read_from_db()
    id = inum_to_id(inum, df_peer)
    print(id)
    try:
        html = urlopen(url).read()
    except:
        return ([], [])
    raw = BeautifulSoup(html).get_text()
    tokens = nltk.word_tokenize(raw)
    text = " ".join(tokens)
    (interest, expertise) = run_lda(text, id = id, from_url= True)


if __name__ == "__main__":
    predict_tags(15)
    #run_lda("The foreign buyer’s tax – in all of its forms and under different governments – never caused strife among voters. It achieved a status that is seldom seem in a province as polarized politically as British Columbia, with NDP voters approving of the actions of Christy Clark in 2016 and BC Liberal voters thinking the current government’s changes were admissible in 2017.")
    #read_from_url('I853966', "https://github.com/mitsuhiko/flask-oauth/issues/96")
    #read_from_db()
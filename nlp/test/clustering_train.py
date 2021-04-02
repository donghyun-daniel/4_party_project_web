# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd
from konlpy.tag import Mecab
from gensim.models import Word2Vec
from textrank import KeywordSummarizer
import operator
from gensim.models import FastText
from sklearn.cluster import KMeans

TEXT_REVIEW_COLUMN_NAME = 'text'
SENTENCE_IDX_COLUME_NAME = 'rawSentenceIdx'
DATA_PATH = 'model/preprocessing/'
OUTPUT_PATH = 'model/keyword_save/'
mecab = Mecab()
models = [['Final_FastText', 8], ['Final_FastText', 17]]

def WordEmbedding_tokenizer(sents):
    word = []
    for sent in sents:
        words = mecab.pos(sent, join=True)
        words = [w.split('/')[0] for w in words if ('/NNG' in w or '/XR' in w or '/NNR' in w)]
        tt = []
        for w in words:
            if len(w) == 1:
                continue
            tt.append(w)
        word.append(tt)
    return word

def mecab_tokenizer(sent):
    words = mecab.pos(sent, join=True)
    words = [w for w in words if ('/NNG' in w or '/XR' in w or '/NNR' in w)]
    word = []
    for item in words:
        if len(item.split('/')[0]) == 1:
            continue
        word.append(item)
    return word

def data_load_df(data):
    data = data.dropna(axis=0)
    rawData = data[TEXT_REVIEW_COLUMN_NAME].values.tolist()
    rawSentenceIdx = data[SENTENCE_IDX_COLUME_NAME].values.tolist()
    tokenData = WordEmbedding_tokenizer(rawData)
    return rawData, tokenData, rawSentenceIdx

def data_load_file(datafilename):
    traindatafile = DATA_PATH + datafilename + '.txt'
    df = pd.read_csv(traindatafile,encoding ='utf-8', sep='\t')
    df = df.dropna(axis=0)
    rawData = df[TEXT_REVIEW_COLUMN_NAME].values.tolist()
    rawSentenceIdx = df[SENTENCE_IDX_COLUME_NAME].values.tolist()
    tokenData = WordEmbedding_tokenizer(rawData)
    return rawData, tokenData, rawSentenceIdx

def Word2Vec_Embedding(tokenData):
    embedding_model = Word2Vec(tokenData, size=64, window = 3, min_count=5, workers=4, iter=20, sg=1)
    word_vectors = embedding_model.wv
    vocabs = word_vectors.vocab.keys()
    word_vectors_list = [word_vectors[v] for v in vocabs]
    return embedding_model, word_vectors, vocabs, word_vectors_list

def FastText_Embedding(tokenData):
    embedding_model = FastText(tokenData, size=64, window=3, min_count=5, workers=4, sg=1, iter=20)
    word_vectors = embedding_model.wv
    return embedding_model, word_vectors

def SentenceMapping(rawData, tokenData, word_vectors, _rawSentenceIdx):
    sentenceData = []
    preRawData = []
    rawSentenceIdx = []
    for idx, i in enumerate(tokenData):
        if len(i) == 0:
            continue
        sentenceData.append(i)
        preRawData.append(rawData[idx])
        rawSentenceIdx.append(_rawSentenceIdx[idx])

    sentenceToken = []
    for sentence in sentenceData:
        n = len(sentence)
        np_arr = np.zeros(shape = word_vectors["화장실"].shape)
        for word in sentence:
            try:
                np_arr += word_vectors[word]
            except:
                pass
        if np_arr.all() == np.zeros:
            continue
        sentenceToken.append(np_arr/n)
    return sentenceToken, preRawData, rawSentenceIdx

def k_means_cluster(sentenceToken, preRawData, rawSentenceIdx, k):
    estimator = KMeans(n_clusters=k, init='k-means++', random_state=42, algorithm='elkan')
    estimator = estimator.fit(sentenceToken)
    cluster_ids_x = estimator.labels_
    cluster_centers = estimator.cluster_centers_
    
    sentence_results = cluster_result_mapping(preRawData, cluster_ids_x, rawSentenceIdx, k)
    keyword_result = cluster_keyword_summarizer(sentence_results, k)

    return keyword_result, sentence_results, cluster_centers

def cluster_result_mapping(data, cluster_estimator, rawSentenceIdx, k):
    results = [[] for _ in range(k)]
    for item, sentenceIdx, label in zip(data, rawSentenceIdx, cluster_estimator):
        results[label].append([item, sentenceIdx])
    return results

def cluster_keyword_summarizer(results, k):
    keyword_extractor = KeywordSummarizer(
        tokenize = mecab_tokenizer,
        min_count=2,
        window=-1,                     # cooccurrence within a sentence
        min_cooccurrence=2,
        vocab_to_idx=None,             # you can specify vocabulary to build word graph
        df=0.85,                       # PageRank damping factor
        max_iter=30,                   # PageRank maximum iteration
        verbose=False
    )
    keyword_result = []
    for i in range(k):
        _tmp = keyword_extractor.summarize([item[0] for item in results[i]], topk=20)
        keyword_result.append(_tmp)
    return keyword_result

def cluster_based_word_counting_in_cluster(embedding_model, cluster_keyword_result, cluster_sentence_result):
    item_list = []
    for keyword, sentences in zip(cluster_keyword_result, cluster_sentence_result):
        item_dic = {}
        cnt = 0
        for item in keyword:
            if cnt == 10:
                break
            try:
                _item = item[0].split('/')[0]
                embedding_model.most_similar(_item, topn=10)
                cnt+=1
                for sentence in sentences:
                    item_dic[_item] = item_dic.get(_item, 0) + sentence[0].count(_item)
            except:
                pass
        item_list.append(item_dic)

    sorted_item_top3 = []
    for item in item_list:
        sort_dict = sorted(item.items(), key=operator.itemgetter(1), reverse=True)
        sorted_item_top3.append(sort_dict[:3])
    print(sorted_item_top3)
    return sorted_item_top3

def keyword_cluster_processing(models, data):
    k = models[1]
    rawData, tokenData, rawSentenceIdx = data_load_df(data)

    embedding_model, word_vectors = FastText_Embedding(tokenData)

    sentenceToken, preRawData, rawSentenceIdx = SentenceMapping(rawData, tokenData, word_vectors, rawSentenceIdx)
    k_cluster_keyword_result, k_cluster_sentence_result, cluster_centroid = k_means_cluster(sentenceToken, preRawData, rawSentenceIdx, k)

    word_counting = cluster_based_word_counting_in_cluster(embedding_model, k_cluster_keyword_result, k_cluster_sentence_result)
    print(word_counting)

    top3Keyword = []   
    for cluster in word_counting:
        top3Keyword.append([item[0] for item in cluster[:3]])   

    word_counting = category_name_change(word_counting)
    print(word_counting)
    category_name = []
    for cluster in word_counting:
        for item, _ in cluster:
            if item == '호텔':
                item = '기타'
            if item == '칫솔' or item == '치약' or item == '수건' or item == '샴푸':
                item = '어메니티'
            category_name.append(item)
            break 
    category_name = np.array(category_name)
    category_name = np.expand_dims(category_name, axis=0)
    top3Keyword = np.array(top3Keyword)
    category = np.concatenate((category_name.T, top3Keyword), axis=1)

    save_model(models[0], k, embedding_model, cluster_centroid)

    return category

def category_name_change(word_counting):
    while True:
        change = 0
        for i in range(len(word_counting)):
            if len(word_counting[i]) == 1:
                continue
            for j in range(i+1, len(word_counting)):
                if len(word_counting[j]) == 1:
                    continue
                if word_counting[j][0][0] == word_counting[i][0][0]:
                    change = 1
                    if word_counting[j][1][1] > word_counting[i][1][1]:
                        word_counting[j].pop(0)
                    else:
                        word_counting[i].pop(0)
        if change == 0:
            break
        
    return word_counting

def save_model(name, k, model, centroid):
    model_filename = OUTPUT_PATH + name + '_' + str(k) + '.model'
    model.save(model_filename)

    npoutfile = OUTPUT_PATH + name + '_' + str(k) + '_vector.npy'
    np.save(npoutfile, centroid)


def keywordCluster(data):
    categories = []
    for model in models:
        category = keyword_cluster_processing(model, data)
        categories.append(category)
    return categories


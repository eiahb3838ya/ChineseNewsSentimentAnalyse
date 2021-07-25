# %%
import os
import re
import json
import pickle
import pandas as pd
import numpy as np
import jieba
from tqdm import tqdm, trange
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import date

tqdm.pandas()

#%% add key terms into jieba to make sure that the key terms will appeal in the dictionary
sentDictFolder = "D:\\work\\profFang\\ChineseNewsSentiment\\00ref\\情緒辭典"
ntusd_negative_terms = pd.read_csv(os.path.join(sentDictFolder, "ntusd-negative.csv")).term
ntusd_positive_terms = pd.read_csv(os.path.join(sentDictFolder, "ntusd-positive.csv")).term
print("negative terms count : {} \npositive terms count : {}".format(len(ntusd_negative_terms),len(ntusd_positive_terms)))
finance_negative_terms = pd.read_csv(os.path.join(sentDictFolder, "FinanceNegative.csv"), index_col=False, names = ['term']).term
finance_positive_terms = pd.read_csv(os.path.join(sentDictFolder, "FinancePositive.csv"), index_col=False, names = ['term']).term
print("negative terms count : {} \npositive terms count : {}".format(len(finance_negative_terms),len(finance_positive_terms)))
terms = pd.concat([ntusd_positive_terms, finance_positive_terms, ntusd_negative_terms, finance_negative_terms])
terms.apply(lambda x: jieba.add_word(x))
terms
# %%
def get_a_corpus(a_content):
    a_content = a_content.strip()
    a_content_list = jieba.cut(a_content, cut_all=False)
    return(" ".join(a_content_list))

#%% main
def main():
    #%% deal with saving path
    tagged_news_data_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\tagged_news_data"
    idf_dict_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\idf_dict"
    scored_news_data_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\scored_news_data"
    filterout_keyterms_dict_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\filterout_keyterms_dict"

    if not os.path.isdir(idf_dict_path):
        os.makedirs(idf_dict_path)

    if not os.path.isdir(scored_news_data_path):
        os.makedirs(scored_news_data_path)

    if not os.path.isdir(filterout_keyterms_dict_path):
        os.makedirs(filterout_keyterms_dict_path) 

    #%% load all the data
    news_file_names = os.listdir(tagged_news_data_path)
    all_data = pd.DataFrame()
    for a_file in news_file_names:
        a_data = pd.read_pickle(os.path.join(tagged_news_data_path, a_file))
        all_data = pd.concat([all_data, a_data])
    all_data = all_data.reset_index()

    #%% fit the vectorizer
    content = all_data.content
    vectorizer = TfidfVectorizer()
    vectorized_content = vectorizer.fit_transform(content.progress_apply(get_a_corpus))
    all_term = vectorizer.get_feature_names()
    idf_dict = dict(zip(all_term, vectorizer.idf_))
    with open(os.path.join(idf_dict_path, '{}.json'.format(date.today())), 'w') as f:
        json.dump(idf_dict, f)


    #%% positive_score
    raw_pos = pd.Series(np.ndarray(len(all_data)))
    positive_terms = all_data.positive_terms
    for i in trange(len(positive_terms)):
        a_terms = positive_terms.iloc[i]
        a_set_key_indices = [vectorizer.vocabulary_.get(a_term, 0) for a_term in a_terms]
        score = vectorized_content[i,a_set_key_indices].sum()
        raw_pos.iloc[i] = score
        

    scaled_pos = (99 *(raw_pos - raw_pos.min())/(raw_pos.max()-raw_pos.min()))+1


    #%% negative_score
    raw_neg = pd.Series(np.ndarray(len(all_data)))
    positive_terms = all_data.negative_terms
    for i in trange(len(positive_terms)):
        a_terms = positive_terms.iloc[i]
        a_set_key_indices = [vectorizer.vocabulary_.get(a_term, 0) for a_term in a_terms]
        score = vectorized_content[i,a_set_key_indices].sum()
        raw_neg.iloc[i] = score

    # scaled_neg = (raw_neg - raw_neg.mean())/raw_neg.std()
    scaled_neg = (99 *(raw_neg - raw_neg.min())/(raw_neg.max()-raw_neg.min()))+1

    # %%
    all_data['positive_score'] = scaled_pos
    all_data['negative_score'] = scaled_neg
    all_data['raw_positive_score'] = raw_pos
    all_data['raw_negative_score'] = raw_neg

    all_data.to_pickle(os.path.join(scored_news_data_path, "scored_news_data_{}.pkl".format(date.today())))


    #%% filterout keyterms
    # pos news
    pos_news = all_data.loc[all_data['positive_score'] > all_data['negative_score']]
    top_positive_terms = pos_news.sort_values("positive_score", ascending = False)[:len(pos_news)//20]['positive_terms']
    filterout_positive_terms = set()
    top_positive_terms.apply(lambda x:[filterout_positive_terms.add(a_term) for a_term in x])

    # neg news
    neg_news = all_data.loc[all_data['positive_score'] < all_data['negative_score']]
    top_negative_terms = neg_news.sort_values("negative_score", ascending = False)[:len(neg_news)//20]['negative_terms']
    filterout_negative_terms = set()
    top_negative_terms.apply(lambda x:[filterout_negative_terms.add(a_term) for a_term in x])

    filterout_keyterms = {"pos_terms":list(filterout_positive_terms), "neg_terms":list(filterout_negative_terms)}

    with open(os.path.join(filterout_keyterms_dict_path, '{}.json'.format(date.today())), 'w') as f:
        json.dump(filterout_keyterms, f)
#%%
if __name__=='__main__':
    main()
    




#%%
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
from cal_sentiment_score import get_a_corpus


#%% deal with saving path
tagged_news_data_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\tagged_news_data"
filterout_keyterms_dict_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\filterout_keyterms_dict"
filterout_keyterms_weight_dict_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\filterout_keyterms_weight_dict"

if not os.path.exists(filterout_keyterms_weight_dict_path):
    os.makedirs(filterout_keyterms_weight_dict_path)
#%% load all the data
news_file_names = os.listdir(tagged_news_data_path)
all_data = pd.DataFrame()
for a_file in news_file_names:
    a_data = pd.read_pickle(os.path.join(tagged_news_data_path, a_file))
    all_data = pd.concat([all_data, a_data])
all_data = all_data.reset_index()

filterout_keyterms_file = os.listdir(filterout_keyterms_dict_path)[-1]

with open(os.path.join(filterout_keyterms_dict_path, filterout_keyterms_file), 'r') as f:
    filterout_keyterms = json.load(f)

#%% fit the vectorizer
content = all_data.content
vectorizer = TfidfVectorizer()
vectorized_content = vectorizer.fit_transform(content.progress_apply(get_a_corpus))
all_term = vectorizer.get_feature_names()


# %% get the weight 
# get sum of tfidf of each term 
all_filtered_out_terms = filterout_keyterms.get("pos_terms")+filterout_keyterms.get("neg_terms")
a_set_key_indices = {a_term:vectorizer.vocabulary_.get(a_term) for a_term in all_filtered_out_terms if vectorizer.vocabulary_.get(a_term) is not None}
a_set_key_weight = {k:vectorized_content[:, v].sum() for k, v in tqdm(a_set_key_indices.items())}

# cal the weight of each term in pos, neg terms respectively
sum_tfidf = np.sum(list(a_set_key_weight.values()))
filterout_keyterms_weight = {}
filterout_keyterms_weight["pos_terms"] = {a_term:a_set_key_weight.get(a_term, 0)/sum_tfidf for a_term in filterout_keyterms.get("pos_terms")}
filterout_keyterms_weight["neg_terms"] = {a_term:a_set_key_weight.get(a_term, 0)/sum_tfidf for a_term in filterout_keyterms.get("neg_terms")}
# %%
# save the result
with open(os.path.join(filterout_keyterms_weight_dict_path, "{}.json".format(date.today())), 'w') as f:
    json.dump(filterout_keyterms_weight, f)
# %%

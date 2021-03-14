#%% import 
import os
import pandas as pd
from tqdm import tqdm
from datetime import date
from random import randrange

#%%
scored_news_data_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\scored_news_data"
scored_news_data_file = os.listdir(scored_news_data_path)[-1]
all_data = pd.read_pickle(os.path.join(scored_news_data_path, scored_news_data_file))
all_data
# %%
categorized_news_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\company_news_data"
merged_news_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\merged_company_news"

if not os.path.exists(merged_news_path):
    os.makedirs(merged_news_path)
if not os.path.exists(os.path.join(merged_news_path, "csv")):
    os.makedirs(os.path.join(merged_news_path, "csv"))
if not os.path.exists(os.path.join(merged_news_path, "h5")):
    os.makedirs(os.path.join(merged_news_path, "h5"))
# %%

company_news_data_filename = os.listdir(os.path.join(categorized_news_path, "h5"))[-1]
to_save_h5 = pd.HDFStore(os.path.join(os.path.join(merged_news_path, "h5"), "{}.h5".format(date.today())))
company_news_data_h5 = pd.HDFStore(os.path.join(os.path.join(categorized_news_path, "h5"), company_news_data_filename))
#%%

to_word_df = pd.DataFrame(columns = ['datetime', 'title', 'source', 'link', 'positive_terms', 'negative_terms', 'positive_score', 'negative_score'])
for a_file_name in tqdm(company_news_data_h5.keys()):
    company_df = company_news_data_h5[a_file_name]
    merged_news_data = pd.merge(company_df, all_data.loc[:, ["link","positive_terms","negative_terms",	"positive_score","negative_score", 'raw_positive_score', 'raw_negative_score']], how="left", on='link')
    save_filename = os.path.join(os.path.join(merged_news_path, "csv"), "{}.csv".format(a_file_name[1:]))
    merged_news_data.to_csv(save_filename)
    to_word_df = pd.concat([to_word_df, merged_news_data.loc[[randrange(0, len(merged_news_data)), randrange(0, len(merged_news_data))], ['datetime', 'title', 'source', 'link', 'positive_terms', 'negative_terms', 'positive_score', 'negative_score']]])
    to_save_h5[a_file_name] = merged_news_data
to_save_h5.close()

# %%

#%% import 
import pandas as pd
from tqdm import tqdm
tqdm.pandas()
import os
#%%
def keyterm_in_content(a_content, keyterm):
    try:
        return(keyterm[keyterm.apply(lambda x :x in a_content)].values)
    except Exception:
        return(pd.Series().values)
# news_df['positive_terms'] = pd.Series()
# a_content = news_df.iloc[0].content
# keyterm = positive_terms
# keyterm_in_content(a_content, keyterm)

# %%
def tag_news_keyterms(news, keyterm):
    if isinstance(news, str):
        try:
            news_df = pd.read_csv(news)
        except FileNotFoundError as fnfe:
            print("check the file path is currect")
            raise fnfe
    else:
        news_df = news
    assert isinstance(
        news_df, pd.DataFrame), "the input news must be df or a path to csv"
    news_df.dropna(inplace=True)
    found_keyterm = news_df['content'].progress_apply(keyterm_in_content, keyterm = keyterm)
    return(found_keyterm)


#%% define main
def main():
    # mkdirs for usage
    news_data_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\news_data\\20210204"
    taggedterms_news_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\tagged_news_data"
    news_filenames = os.listdir(news_data_path)
    if not os.path.exists(taggedterms_news_path):
        os.makedirs(taggedterms_news_path)

    #%% load dictionary
    sentDictFolder = "D:\\work\\profFang\\ChineseNewsSentiment\\00ref\\情緒辭典"
    ntusd_negative_terms = pd.read_csv(os.path.join(sentDictFolder, "ntusd-negative.csv")).term
    ntusd_positive_terms = pd.read_csv(os.path.join(sentDictFolder, "ntusd-positive.csv")).term
    print("negative terms count : {} \npositive terms count : {}".format(len(ntusd_negative_terms),len(ntusd_positive_terms)))
    
    finance_negative_terms = pd.read_csv(os.path.join(sentDictFolder, "FinanceNegative.csv"), index_col=False, names = ['term']).term
    finance_positive_terms = pd.read_csv(os.path.join(sentDictFolder, "FinancePositive.csv"), index_col=False, names = ['term']).term
    print("negative terms count : {} \npositive terms count : {}".format(len(finance_negative_terms),len(finance_positive_terms)))

    positive_terms = pd.concat([ntusd_positive_terms, finance_positive_terms])
    negative_terms = pd.concat([ntusd_negative_terms, finance_negative_terms])
    
    # find key terms of each file
    for a_file in news_filenames:
        a_newspath = os.path.join(news_data_path, a_file)
        news_df = pd.read_csv(a_newspath)
        news_df.dropna(inplace=True)

        #%% tag terms with function above
        news_df['positive_terms'] = tag_news_keyterms(news_df, positive_terms)
        news_df['negative_terms'] = tag_news_keyterms(news_df, negative_terms)

        #%% save to pickle
        news_df.to_pickle(os.path.join(taggedterms_news_path, "tagged_"+a_file.replace(".csv", ".pkl")))
# %% main
if __name__ == '__main__':
    main()
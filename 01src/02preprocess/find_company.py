# %% import
import pandas as pd
from tqdm import tqdm, trange
from multiprocessing import Pool, cpu_count
from datetime import date

# %%
def prepare_keyterm_dict(etf_df, key, *terms):
    keyterm = dict()
    for i in range(len(etf_df)):
        a_row = etf_df.iloc[i]
        if type(a_row[key]) == str:
            keyterm[a_row[key]] = [a_row[a_term].replace(
                " ", "") for a_term in terms if type(a_row[a_term]) == str]
    return(keyterm)
# %%


def single_company_news(news_df, *terms):
    this_company_news = pd.DataFrame()
    for i in trange(len(news_df), desc=terms[0]):
        a_news = news_df.iloc[i]
        for term in terms:
            if (term in a_news.content):
                this_company_news = pd.concat(
                    [this_company_news, a_news], axis=1)
    return(this_company_news.T)


def categorize_company_news(news, keyterm):
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
    company_news_dict = dict()
    for k, v in keyterm.items():
        company_news_dict[k] = single_company_news(news_df, *v)
    return(company_news_dict)


# %%
if __name__ == "__main__":
    #%%
    etf100_df = pd.read_csv(
        "D:\\work\\profFang\\ChineseNewsSentiment\\00ref\\ETF成分股\\深证100etf-公司查询.csv", dtype=str)
    etf50_df = pd.read_csv(
        "D:\\work\\profFang\\ChineseNewsSentiment\\00ref\\ETF成分股\\上证50etf-公司查询.csv", dtype=str)
    etf_df = pd.concat([etf100_df, etf50_df])

    key = "证券代码"
    terms = ["证券代码", "股票简称", "董事长"]
    keyterm = prepare_keyterm_dict(etf_df, key, *terms)

    import os
    news_data_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\news_data\\20210204"
    categorized_news_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\company_news_data"
    news_filenames = os.listdir(news_data_path)
    if not os.path.exists(categorized_news_path):
        os.makedirs(categorized_news_path)
    if not os.path.exists(os.path.join(categorized_news_path, "csv")):   
        os.makedirs(os.path.join(categorized_news_path, "csv"))
    if not os.path.exists(os.path.join(categorized_news_path, "h5")): 
        os.makedirs(os.path.join(categorized_news_path, "h5"))
    #%% 

    h5file = os.path.join(os.path.join(
        categorized_news_path, "h5"), "{}.h5".format(date.today()))
    h5 = pd.HDFStore(h5file)
    for a_news_file in news_filenames:
        print(a_news_file)
        a_newspath = os.path.join(news_data_path, a_news_file)
        a_company_news_dict = categorize_company_news(a_newspath, keyterm)

        for k, v in a_company_news_dict.items():
            csvfile = os.path.join(os.path.join(
                categorized_news_path, "csv"), "{}.csv".format(k))
            if not os.path.isfile(csvfile):
                v.to_csv(csvfile, index = False)
                h5.put(k, v)
            else:
                v.to_csv(csvfile, index = False, mode='a', header=False)
                h5[k] = pd.concat([h5[k],v])
    h5.close()


# %%

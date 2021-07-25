# %%
import os
import pandas as pd
import statsmodels.api as sm
from tqdm import tqdm
# %%
market_sentiment_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\market_sentiment"
market_sentiment = pd.read_csv(os.path.join(market_sentiment_path, "market_sentiment.csv"))

merged_news_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\merged_company_news"
merged_h5_file = os.listdir(os.path.join(merged_news_path, "h5"))[-1]
merged_h5 = pd.HDFStore(os.path.join(os.path.join(merged_news_path, "h5"), merged_h5_file))

ios_ips_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\ios_ips_Y"
ios_path = os.path.join(ios_ips_path, "ios")
ips_path = os.path.join(ios_ips_path, "ips")
adj_ios_path = os.path.join(ios_ips_path, "adj_ios")
adj_ips_path = os.path.join(ios_ips_path, "adj_ips")

if not os.path.exists(ios_ips_path):
    os.makedirs(ios_ips_path)
if not os.path.exists(ios_path):
    os.makedirs(ios_path)
if not os.path.exists(ips_path):
    os.makedirs(ips_path)

if not os.path.exists(adj_ios_path):
    os.makedirs(adj_ios_path)
if not os.path.exists(adj_ips_path):
    os.makedirs(adj_ips_path)


# %%
market_sentiment.index = pd.to_datetime(market_sentiment.years.apply(lambda x:str(pd.to_datetime(x).year)+"-12-31"), format="%Y-%m-%d")
market_sentiment = market_sentiment.drop(columns=["years"])
# a_asset = merged_h5.keys()[0]
# a_news_df = merged_h5.get(a_asset)
# %%
def scaled(raw_neg:pd.Series):
    scaled_neg = (99 *(raw_neg - raw_neg.min())/(raw_neg.max()-raw_neg.min()))+1
    return(scaled_neg)


def get_resid(a_column:pd.Series):
    Y = a_column.dropna().values
    X = market_sentiment.loc[a_column.dropna().index]
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()
    adj_ios = pd.Series(results.resid.values, index=X.index)
    # print("resid of ios is\n", adj_ios)
    return(adj_ios)


# %%
all_ios = pd.DataFrame()
all_ips = pd.DataFrame()
for a_asset in tqdm(merged_h5.keys()):
    a_news_df = merged_h5.get(a_asset)
    a_news_df.datetime = pd.to_datetime(a_news_df.datetime)
    pos_news_df = a_news_df.loc[a_news_df.positive_score > a_news_df.negative_score]
    ios = pos_news_df.groupby(pd.Grouper(key='datetime',freq='Y')).sum()
    ios = ios.iloc[:, :2]
    ios.columns = ["positive_sum", "negative_sum"]
    all_ios[a_asset[1:]]=ios["positive_sum"]

    neg_news_df = a_news_df.loc[a_news_df.positive_score > a_news_df.negative_score]
    ips = neg_news_df.groupby(pd.Grouper(key='datetime',freq='Y')).sum()
    ips = ips.iloc[:, :2]
    ips.columns = ["positive_sum", "negative_sum"]
    all_ips[a_asset[1:]]=ios["negative_sum"]

#%%
all_ios = all_ios.apply(scaled, axis=0)
all_ios.to_csv(os.path.join(ios_path, "{}.csv".format("all_ios")))

all_ios = all_ios.drop(pd.to_datetime("2021-12-31"), axis=0)
adj_ios = all_ios.apply(get_resid)
adj_ios.to_csv(os.path.join(adj_ios_path, "{}.csv".format("adj_ios")))

all_ips = all_ips.apply(scaled, axis=0)
all_ips.to_csv(os.path.join(ips_path, "{}.csv".format("all_ips")))

all_ips = all_ips.drop(pd.to_datetime("2021-12-31"), axis=0)
all_ips = all_ips.apply(get_resid)
all_ips.to_csv(os.path.join(adj_ips_path, "{}.csv".format("adj_ips")))
# %%

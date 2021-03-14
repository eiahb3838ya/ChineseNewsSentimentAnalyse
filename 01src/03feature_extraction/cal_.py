# %%
import os
import pandas as pd

# %%
merged_news_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\merged_company_news"
merged_h5_file = os.listdir(os.path.join(merged_news_path, "h5"))[-1]
merged_h5 = pd.HDFStore(os.path.join(os.path.join(merged_news_path, "h5"), merged_h5_file))

ios_ips_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\ios_ips_Y"
ios_path = os.path.join(ios_ips_path, "ios")
ips_path = os.path.join(ios_ips_path, "ips")

if not os.path.exists(ios_ips_path):
    os.makedirs(ios_ips_path)
if not os.path.exists(ios_path):
    os.makedirs(ios_path)
if not os.path.exists(ips_path):
    os.makedirs(ips_path)

# %%
a_asset = merged_h5.keys()[0]
a_news_df = merged_h5.get(a_asset)
# %%
for a_asset in merged_h5.keys():
    a_news_df = merged_h5.get(a_asset)
    a_news_df.datetime = pd.to_datetime(a_news_df.datetime)
    pos_news_df = a_news_df.loc[a_news_df.positive_score > a_news_df.negative_score]
    ios = pos_news_df.groupby(pd.Grouper(key='datetime',freq='Y')).sum()
    ios = ios.iloc[:, :2]
    ios.columns = ["positive_sum", "negative_sum"]
    ios.to_csv(os.path.join(ios_path, "{}.csv".format(a_asset[1:])))

    neg_news_df = a_news_df.loc[a_news_df.positive_score > a_news_df.negative_score]
    ips = neg_news_df.groupby(pd.Grouper(key='datetime',freq='Y')).sum()
    ips = ips.iloc[:, :2]
    ips.columns = ["positive_sum", "negative_sum"]
    ips.to_csv(os.path.join(ips_path, "{}.csv".format(a_asset[1:])))

# %%

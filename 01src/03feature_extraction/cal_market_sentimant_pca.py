# %%
import os
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA

# %%
raw_market_sentiment_path = "D:\\work\\profFang\\ChineseNewsSentiment\\00ref\\四個市場情緒變數-2021.05.09.csv"
market_sentiment_path = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\market_sentiment"
if not os.path.exists(market_sentiment_path):
    os.makedirs(market_sentiment_path)

# %%
raw_market_sentiment = pd.read_csv(raw_market_sentiment_path, parse_dates=[0], index_col=0)
raw_market_sentiment = raw_market_sentiment.dropna(axis = 1, how='all').dropna(axis = 0, how='any')
raw_market_sentiment['ln_CFED_t'] = np.log(raw_market_sentiment['CFED_t'])
raw_market_sentiment = raw_market_sentiment.drop(columns=['CFED_t'])
# %%
pca = PCA(n_components=1)
market_sentiment = raw_market_sentiment.copy()
market_sentiment["market_sentiment"] = pca.fit_transform(raw_market_sentiment)
# %%
market_sentiment.to_csv(os.path.join(market_sentiment_path, "market_sentiment.csv"))
# %%
list(zip(market_sentiment.columns, pca.components_[0]))
# %%
pca.explained_variance_ratio_
# %%

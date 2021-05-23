#%%
import os
import pandas as pd
import numpy as np
import statsmodels.api as sm
from tqdm import tqdm

# %%
DATA_ROOT = "D:\\work\\profFang\\ChineseNewsSentiment\\00ref"
TO_SAVE = "D:\\work\\profFang\\ChineseNewsSentiment\\02data"

sh_share_weekly_return = pd.read_csv(os.path.join(DATA_ROOT, "zz_share_weeklyreturn.csv"),parse_dates=[2], na_values="        -")
sh_index_return = pd.read_csv(os.path.join(DATA_ROOT, "zz_index return.csv"), parse_dates=[2], na_values="        -")

sh_share_weekly_return.columns = ["asset", "name", "date", "return"]
sh_index_return.columns = ["asset", "name", "date", "return"]
# sh_share_weekly_return.date = pd.to_datetime(sh_share_weekly_return.date, format="%y%m%d"

sh_share_weekly_return = sh_share_weekly_return.set_index(["date", "asset"])['return'].astype(np.float32)
sh_index_return = sh_index_return.set_index(["date", "asset"])['return'].astype(np.float32)
index_return = sh_index_return.reset_index('asset', drop=True)
#%%
def f(df):
    this_date = df['date']
    index_return_indexer = index_return.index.get_loc(this_date)
    to_regress = index_return.iloc[index_return_indexer-2:index_return_indexer+3]
    if len(to_regress)<5:
        return(pd.Series([np.nan] *5,index = ['t-2', "t-1", 't', 't+1', 't+2'], name=this_date))
    else:
        to_regress.index = ['t-2', 't-1', 't', 't+1', 't+2']
        to_regress.name = this_date
        return(to_regress)
        


# %%
# index_return = sh_index_return.reset_index(1, drop="True")
# a_group = sh_share_weekly_return.groupby(level = 'asset').get_group(1)

def get_resid(a_group):
    to_regress = pd.DataFrame(a_group.reset_index().apply(f, axis = 1).values, index = a_group.index)
    # print(pd.concat([a_group, to_regress], axis=1).head())
    data = pd.concat([a_group, to_regress], axis=1).astype(np.float32).dropna()
    Y = data.iloc[:, 0]
    X = data.loc[:, [0,1,2,3,4]]
    X = sm.add_constant(X)
    if len(Y)>0:
        model = sm.OLS(Y,X)
        results = model.fit()
        return(results.resid)
    else:
        return(pd.Series())
# get_resid(a_group)
# %%
groups = sh_share_weekly_return.groupby(level = 'asset')
res = {}
for name, a_group in tqdm(groups):
    res[name] = get_resid(a_group)

# %%
def ncscrew(s):
    n = len(s)
    sum_1 = s.pow(3).sum()
    sum_2 = s.pow(2).sum()
    upper = -(n*(n-1)**(3/2)*sum_1)
    down = (n-1)*(n-2)*sum_2**(3/2)
    try:
        return(upper/down)
    except ZeroDivisionError:
        print("0 error")
        return(np.nan)
    except Exception:
        raise
    

ncscrew_res = {}
for name, e in (res.items()):
    w = np.log(1 + e/100)
    if len(e):
        ncscrew_res[name] = w.groupby(pd.Grouper(level='date',freq='Y')).apply(lambda s:ncscrew(s))
# %%
all_res = []
for name, df in ncscrew_res.items():
    df.index = pd.MultiIndex.from_product([[name],df.index])
    all_res.append(df)
# %%
if not os.path.exists(os.path.join(TO_SAVE, "crash")):
    os.makedirs(os.path.join(TO_SAVE, "crash"))
pd.concat(all_res).to_csv(os.path.join(os.path.join(TO_SAVE, "crash"), "zz_ncscrew.csv"))
# %%

def decide_up_down(df):
    df = df.reset_index(1, drop=True)
    output = df>sh_index_return_s.loc[df.index]
    return output

sh_index_return_s = sh_index_return.reset_index(1, drop=True)
sh_up_down = sh_share_weekly_return.groupby(level='asset').apply(decide_up_down)
#%%
def duvol(s, company_up_down):
    # print(s)
    df = pd.merge(s.rename('tmp').reset_index(1,drop = True), company_up_down, left_index=True, right_index = True)
    nu = (df.iloc[:, 1].sum()-1)
    nd = ((~df.iloc[:, 1]).sum()-1)
    up_sum = df.ix[df.iloc[:, 1],0].pow(2).sum()
    down_sum = df.ix[~df.iloc[:, 1],0].pow(2).sum()
    return(np.log(nu*down_sum/nd/up_sum))

duvol_res = {}
for name, e in (res.items()):
    w = np.log(1 + e/100)
    if len(e):
        duvol_res[name] = w.groupby(pd.Grouper(level='date',freq='Y')).apply(lambda s:duvol(s, sh_up_down.xs(name, 0)))
# %%
# %%
all_res = []
for name, df in duvol_res.items():
    df.index = pd.MultiIndex.from_product([[name],df.index])
    all_res.append(df)
# %%
if not os.path.exists(os.path.join(TO_SAVE, "crash")):
    os.makedirs(os.path.join(TO_SAVE, "crash"))
pd.concat(all_res).to_csv(os.path.join(os.path.join(TO_SAVE, "crash"), "zz_duvol_res.csv"))
# %%

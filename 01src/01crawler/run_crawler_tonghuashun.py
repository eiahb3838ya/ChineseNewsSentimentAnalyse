#%%
import os
from datetime import datetime
from SinaCrawler import SinaCrawler
from LuoJiaInvestCrawler import LuoJiaInvestCrawler
from FinanceChinaCrawler import FinanceChinaCrawler
from TongHuaShunCrawler import TongHuaShunCrawler
from logger import Logger


SAVE_PATH = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\news_data\\{}".format(datetime.now().strftime("%Y%m%d"))
LOGGER_PATH = "D:\\work\\profFang\\ChineseNewsSentiment\\01src\\01crawler\\log"
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

#%%
def main():
    logger = Logger(LOGGER_PATH, "news_crawling")
    sc = TongHuaShunCrawler(SAVE_PATH,10220+20965-20482,20965,logger)
    sc.run('companynews_list')
    sc = TongHuaShunCrawler(SAVE_PATH,1,1690,logger)
    sc.run('today_list')

# %%
if __name__ == "__main__":
    main()

# %%

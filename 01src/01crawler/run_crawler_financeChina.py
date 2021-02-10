#%%
import os
from datetime import datetime
from SinaCrawler import SinaCrawler
from LuoJiaInvestCrawler import LuoJiaInvestCrawler
from FinanceChinaCrawler import FinanceChinaCrawler
from logger import Logger

SAVE_PATH = "D:\\work\\profFang\\ChineseNewsSentiment\\02data\\news_data\\{}".format(datetime.now().strftime("%Y%m%d"))
LOGGER_PATH = "D:\\work\\profFang\\ChineseNewsSentiment\\01src\\01crawler\\log"
if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

#%%
def main():
    logger = Logger(LOGGER_PATH, "news_crawling")

    # index_link_dict = {
    #     "ssgs":"http://app.finance.china.com.cn/news/column.php?cname=%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8",
    #     "zqyw":"http://app.finance.china.com.cn/news/column.php?cname=证券要闻",
    #     "dpfx":"http://app.finance.china.com.cn/news/column.php?cname=大盘分析"
    # }

    fc = FinanceChinaCrawler(SAVE_PATH,1,270,logger)
    fc.run("ssgs")
    fc.run("zqyw")
    fc.run("dpfx")


    

# %%
if __name__ == "__main__":
    main()

# %%


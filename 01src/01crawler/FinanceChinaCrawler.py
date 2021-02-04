#%% 

import logging
import datetime
import requests, os
from bs4 import BeautifulSoup
import pandas as pd


#%%
class FinanceChinaCrawler(object):
    index_link_dict = {
        "ssgs":"http://app.finance.china.com.cn/news/column.php?cname=%E4%B8%8A%E5%B8%82%E5%85%AC%E5%8F%B8",
        "zqyw":"http://app.finance.china.com.cn/news/column.php?cname=证券要闻",
        "dpfx":"http://app.finance.china.com.cn/news/column.php?cname=大盘分析"
    }
    def __init__(self, save_file_path, start_page = None, end_page = None, logger = None):
        self.save_file_path = save_file_path
        self.soup = None
        if not os.path.exists(save_file_path):
            os.makedirs(save_file_path)

        if logger == None:
            self.logger = logging.getLogger()
        else:
            self.logger = logger
        if start_page == None:
            self.start_page = 1
        else:
            self.start_page = start_page

        if start_page == None:
            self.end_page = 500
        else:
            self.end_page = end_page


    def get_link_content(self, link):
        # connection error
        try:
            link_res=requests.get(link)
        except Exception as e:
            self.logger.warning(str(e))
            self.logger.warning("page not found")
            return(None)

        link_res.encoding=('utf8')
        link_html=link_res.text
        link_soup=BeautifulSoup(link_html, 'html.parser')
        link_artibody=link_soup.find("div",id="fontzoom")

        if not link_artibody:
            self.logger.debug("link_artibody id: fontzoom fail")
            link_artibody = link_soup.find("div",id="content")
        try:
            link_p=",".join([p.text.strip() for p in link_artibody.findAll("p")])
        except Exception as e:
            self.logger.warning("nothing in link_p")
            link_p=""

        link_time_str=""
        try:
            link_span_time2=link_soup.find("span",class_="fl time2")
            link_time_str=link_span_time2.text.strip()[:16]
        except Exception as e:
            self.logger.debug(str(e)+"the link_time is old version")


        old = False
        # deal with old version web page
        if len(link_time_str)==0:
            try:
                link_span_time2=link_soup.find("span",id="pubtime_baidu")
                link_time_str=link_span_time2.text.strip()[5:]
            except Exception as e:
                self.logger.warning(str(e)+"use new version to match time still fail")
            old = True
    
        if len(link_time_str)==0:
            self.logger.warning("nothing in link_time")
            link_time_dt = ""
        else:
            try:
                if not old:
                    link_time_dt=datetime.datetime.strptime(link_time_str,"%Y年%m月%d日%H:%M")
                elif old:
                    # 2016-04-08 14:51:58
                    link_time_dt=datetime.datetime.strptime(link_time_str,"%Y-%m-%d %H:%M:%S")
            except Exception as e:
                self.logger.warning("link_time doesn't match")
                link_time_dt=""
        return(link_p,link_time_dt)

    def get_dict_list(self, ul_list):
        try:
            a_list=ul_list.findAll('a')
        except Exception as e:
            print(str(e))
            a_list=[]
        # dict_list_finance_china=[]
        dict_list=[]
        for a_a in a_list:
            a_title=a_a.text
            self.logger.debug("news title: "+a_title)

            a_link=a_a.get('href')
            self.logger.debug("news link: "+a_link)
            
            a_content,a_time_dt=self.get_link_content(a_link)

            if a_content and a_time_dt:
                self.logger.debug(a_link+" ...done")
            else:
                self.logger.debug(a_link+" ...fail")

            a_dict={
                "datetime":a_time_dt,
                "title":a_title,
                "link":a_link,
                "content":a_content,
                "source" : "finaceChina"
                }
            dict_list.append(a_dict)
        return(dict_list)

    def one_page_process(self, req_link):
        self.logger.info("req new page of :"+req_link)
        # connection error
        try:
            res=requests.get(req_link)
        except Exception as e:
            self.logger.warning(str(e))
            self.logger.warning("the page not found")
            return(None, None)

        res.encoding=('utf8')
        html_doc=res.text
        self.soup = BeautifulSoup(html_doc, 'html.parser')
        ul_list=self.soup.find("ul",class_="news_list")
        if not ul_list:
            self.logger.warning("there's no ul_list")

        dict_list=self.get_dict_list(ul_list)
        all_df=pd.DataFrame(dict_list,columns=["datetime","title","content","link","source"])
        return(all_df, dict_list)

    def save_content(self, all_df, filename = "finance_china", *args):
        file_name = "{}.csv".format("_".join([filename]+list(args)))
        file_path = os.path.join(self.save_file_path, file_name)
        if (os.path.isfile(file_path)):
            all_df.to_csv(file_path,mode="a",index_label="id", header=False)
            self.logger.info("append csv page to: {}".format(file_path))
        else:
            all_df.to_csv(file_path,mode="a",index_label="id")
            self.logger.info("new write page to: {}".format(file_path))
    
    def run(self, type_):
        req_link = "{}&p={}".format(self.index_link_dict[type_],str(self.start_page))
        for page in range(self.start_page, self.end_page+1):
            all_df, dict_list = self.one_page_process(req_link)
            if not isinstance(all_df, pd.DataFrame) or len(dict_list) <= 0:break
            else:
                klass.save_content(all_df, "finance_china", type_)
                next_a=self.soup.find("ul",class_="page").findAll("li")[1].a
                req_link=next_a.get("href")

                if len(req_link)<=0:
                    break
                elif req_link.startswith("/news/"):
                    req_link="http://app.finance.china.com.cn"+req_link










# %%
if __name__ == "__main__":
    from logger import Logger
    logger = Logger("tmp","tmp")
    klass = FinanceChinaCrawler("tmp",1,5)
    klass.run('ssgs')
    

# %%

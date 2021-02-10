#%%    

import requests, json
import time
import logging
import datetime
import requests, os
from bs4 import BeautifulSoup
import pandas as pd

#%%

class HeXunCrawler(object):
    index_link = "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp"
    q = "?id=184571007&s=100&cp={}&priority=0&callback="
    def __init__(self, save_file_path, start_page = None, end_page = None, logger = None):
        self.save_file_path = save_file_path
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

    def one_page_process(self, req_link):
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            res = requests.get(req_link, headers=headers)

        except Exception as e:
            self.logger.warning(str(e))
            self.logger.warning("the page not found")
            return(None, None)
        html_doc = res.text
        resjson = json.loads(html_doc)
        try:
            result_list = resjson['result']
        except:
            self.logger.warning("there's no ul_list")
            print("there's no ul_list")
            return(None, None)

        dict_list=self.get_dict_list(result_list)

        all_df=pd.DataFrame(dict_list,columns=["datetime","title","content","link","source"])
        return(all_df, dict_list)


    def get_dict_list(self, ul_list):
        dict_list = []
        for a_dict in ul_list:
            time.sleep(0.25)
            a_title=a_dict.get("title")
            self.logger.debug("news title: "+a_title)
            a_link=a_dict.get('entityurl')
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
                "source" : "hexun"
            }
            dict_list.append(a_dict)
        return(dict_list)

    def get_link_content(self, link):
        # connection error
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            link_res = requests.get(link, headers=headers)

        except Exception as e:
            self.logger.warning(str(e))
            self.logger.warning("page not found")
            return(None, None)

        link_res.encoding=('gb2312')
        link_html=link_res.text
        link_soup=BeautifulSoup(link_html, 'html.parser')
        link_main_div=link_soup.find("div",class_="art_contextBox")
        try:
            link_p=",".join([p.text.strip() for p in link_main_div.findAll("p")])
        except Exception as e:
            self.logger.warning("nothing in link_p for link {}".format(link))
            link_p=""

        link_time_str=""
        try:
            link_span_time=link_soup.find("span",class_="pr20")
            link_time_str=link_span_time.text.strip()
        except Exception as e:
            # self.logger.debug(str(e)+"the link_time is old version")
            pass

        if len(link_time_str) == 0:
            self.logger.warning("nothing in link {}".format(link))
            link_time_dt = ""
        else:
            try:
                link_time_dt=datetime.datetime.strptime(link_time_str,"%Y-%m-%d %H:%M:%S")
            except Exception as e:
                self.logger.warning("link_time doesn't match")
                link_time_dt=""
        return(link_p, link_time_dt)

    def save_content(self, all_df, filename = "HeXun", *args):
        file_name = "{}.csv".format("_".join([filename]+list(args)))
        file_path = os.path.join(self.save_file_path, file_name)
        if (os.path.isfile(file_path)):
            all_df.to_csv(file_path,mode="a",index_label="id", header=False)
            self.logger.info("append csv page to: {}".format(file_path))
        else:
            all_df.to_csv(file_path,mode="a",index_label="id")
            self.logger.info("new write page to: {}".format(file_path))
    
    def run(self, type_=None):
        # index_link = "http://open.tool.hexun.com/MongodbNewsService/newsListPageByJson.jsp
        # q = "?id=184571007&s=100&cp={}&priority=0&callback="
        for page_num in range(self.start_page,self.end_page+1):
            time.sleep(1)
            req_link = self.index_link+self.q.format(page_num)
            self.logger.info("request new page of :"+req_link)
            all_df, dict_list = self.one_page_process(req_link)
            if not isinstance(all_df, pd.DataFrame) or len(dict_list) <= 0:continue
            else:
                self.save_content(all_df, "HeXun")

#%% main
if __name__ == "__main__":
    from logger import Logger
    logger = Logger("tmp","tmp")
    klass = HeXunCrawler("tmp",1,3,logger)
    klass.run()

# %%

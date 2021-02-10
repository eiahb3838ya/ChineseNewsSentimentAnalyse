#%% 

import logging
import datetime
import requests, os
from bs4 import BeautifulSoup
import pandas as pd


#%%
class SinaCrawler(object):
    index_link_dict = {
        "stock":"http://finance.sina.com.cn/roll/index.d.html?cid=56588",
        "company":"http://finance.sina.com.cn/roll/index.d.html?cid=56592"
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
            return("","")

        link_res.encoding=('utf8')
        link_html=link_res.text
        link_soup=BeautifulSoup(link_html, 'html.parser')
        link_artibody=link_soup.find("div",id="artibody")
        try:
            link_p=",".join([p.text.strip() for p in link_artibody.findAll("p")])
        except Exception as e:
            self.logger.warning(str(e))
            self.logger.warning("nothing in link_p")
            link_p=""


        link_time_str=""
        link_time = link_soup.find("span",class_="date")
        try:
            link_time_str = link_time.text
        except:
            self.logger.warning("link_time not found:"+link)

        # use better way later to get time
        if len(link_time_str)==0:
            self.logger.warning("nothing in link_time")
            link_time_dt = ""
        else:
            try:
                link_time_dt=datetime.datetime.strptime(link_time_str,"%Y年%m月%d日 %H:%M")
            except Exception as e:
                self.logger.warning("link_time doesn't match")
                link_time_dt=""
        return(link_p,link_time_dt)

    def get_dict_list(self, ul_list):
        dict_list=[]
        for a_ul in ul_list:
            a_list=a_ul.findAll('a')
            for a_a in a_list:
                a_title=a_a.text
                self.logger.debug("news title: "+a_title)

                a_link=a_a.get('href')
                self.logger.debug("news link: "+a_link)
                
                a_content,a_datetime=self.get_link_content(a_link)

                
                if a_content and a_datetime:
                    self.logger.debug(a_link+" ...done")
                else:
                    self.logger.debug(a_link+" ...fail")

                a_dict={
                    "datetime":a_datetime,
                    "title":a_title,
                    "link":a_link,
                    "content":a_content,
                    "source":"sinaStock"
                    }
                dict_list.append(a_dict)
        return(dict_list)

    def one_page_process(self, req_link):
        try:
            res=requests.get(req_link)
        except Exception as e :
            self.logger.warning(str(e))
            self.logger.warning("the page not found")
            return(None, None)

        res.encoding=('utf8')
        html_doc=res.text
        soup = BeautifulSoup(html_doc, 'html.parser')

        ul_list=soup.findAll('ul',class_="list_009")
        
        if not ul_list:
            self.logger.warning("there's no ul_list")

        dict_list=self.get_dict_list(ul_list)
        all_df=pd.DataFrame(dict_list,columns=["datetime","title","content","link","source"])

        return(all_df, dict_list)

    def save_content(self, all_df, filename = "sina", *args):
        file_name = "{}.csv".format("_".join([filename]+list(args)))
        file_path = os.path.join(self.save_file_path, file_name)
        if (os.path.isfile(file_path)):
            all_df.to_csv(file_path,mode="a",index_label="id", header=False)
            self.logger.info("append csv page to: {}".format(file_path))
        else:
            all_df.to_csv(file_path,mode="a",index_label="id")
            self.logger.info("new write page to: {}".format(file_path))
    
    def run(self, type_=None):
        if type_ == None:
            type_ = 'stock'
        for page_num in range(self.start_page,self.end_page+1):
            req_link=self.index_link_dict[type_]+"&page="+str(page_num)
            self.logger.info("request new page of :"+req_link)
            all_df, dict_list = self.one_page_process(req_link)
            if not isinstance(all_df, pd.DataFrame) or len(dict_list) <= 0:continue
            else:
                self.save_content(all_df, "sina", type_)











# %%
if __name__ == "__main__":
    from logger import Logger
    logger = Logger("tmp","tmp")
    klass = SinaCrawler("tmp",1,3,logger)
    klass.run("stock")

    

# %%

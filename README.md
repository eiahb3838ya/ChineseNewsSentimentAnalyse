ChineseNewsSentimentAnalyse
==============================
# 1. 爬蟲
「第一阶段」：互联网爬虫搜集资料的属性、平台
资料来源于五个投资平台
分别是
1. 珞珈投资
2. 中国网财经
3. 新浪财经
4. 同花顺财经
5. 和讯股票

使用 runXxxxxCrawler 就可以開啟對應的爬蟲的 class
https://github.com/eiahb3838ya/ChineseNewsSentimentAnalyse/tree/master/01src/01crawler


# 2. 查找新聞中提及公司名與已有情緒辭典
1. 將新聞歸類於各個公司
    替上證50 與 深證100 etf 成分股中股票查找新聞
    每個公司都建立新聞庫供後續使用   https://github.com/eiahb3838ya/ChineseNewsSentimentAnalyse/tree/master/01src/02preprocess/find_company.py


2. 情緒辭典的選擇
    有分為一般性情緒辭典(台大)跟金融類情緒辭典(廈門大學)


|    name    | source |file position
| ---------- | ---------| ----------
| 台湾大学简体中文情感极性词典ntusd |  https://reurl.cc/mdn94W |00ref\情緒辭典|
| 中文財務情緒字典 |https://clip.csie.org/10K/publications |00ref\情緒辭典|

將每則新聞找出已知情緒詞並且存起來
https://github.com/eiahb3838ya/ChineseNewsSentimentAnalyse/tree/master/01src/02preprocess/find_keyterms.py

3. idf 情緒分數     
    我們使用 idf 的方法替每一個情緒詞進行打分
    每個詞都有一個分數可以詳見於 02data\idf_dict 可以找到每個詞的分數
    對於每個新聞我們都查找對應關鍵詞的 tfidf 分數
    將正向詞語的 tfidf 分數相加並正規化得正向分數
    將負向詞語的 tfidf 分數相加並正規化得負向分數
4. 篩選出有用的正負特徵詞     
    如果第k则新闻中的乐观特征词的得分高于悲观特征词的得分，则该新闻按乐观类别进行分类; 我们选择具有前5％分数的新闻的特征词作为我们的正向特征词。反之。该新闻按悲观类进行分类。同样，我们选择那些后5％得分的信息作为我们的负向特征词。
    利用情緒辭典找出極端正負新聞的分數(搜集所有潛在的特徵詞)做為我們的標註依據
  -  前5% (樂觀)：包括:
     '开发',
     '开心',
     '开拓',
     '开放',
     '开放的',
     '开采',
     '异常',
     '强',
     '强度',
     '当然',
     '影响',
     '得天独厚',
     '微妙',
     '微妙的',
     '微微',
     '德高望重',
     '心动',等等
  -  後5% (悲觀)：包括: 
     '崩溃',
     '责成',
     '确定',
     '无用的',
     '不能',
     '可靠',
     '秘密的',
     '无序',
     '敏感性',
     '负荷',
     '沉寂',
     '可疑的',
     '困难的',
     '捏造',
     '入侵',等等
 
  -  標註完成在: 02data\filterout_keyterms_dict


---  
3. 特徵詞的每一則新聞字數打散，進行卡方獨立性檢定:
經過卡方檢定(alpha = 0.05)者:
03featureExtraction_featureSelection/selected_neg_table.csv
03featureExtraction_featureSelection/selected_pos_table.csv


4. 利用TF-IDF方法計算IOS跟IPS：
此階段計算投資人在某月t對ith
廠商的“樂觀情緒密度”(IOSit)及“悲觀情緒密度”(IPSit)。藉由對樂觀情緒計算特徵詞，量化投資人對特定廠商的樂觀情緒之程度。本計畫首先將投資人每篇對ith廠商樂觀情緒、jth特徵詞的詞頻 、TF乘以相對應的權重
，並累積對樂觀情緒的所有代表性特徵詞，計算為每篇IOS(IOSidk)。
接續，我加總每篇的IOS計算為每月的IOS, 並加總每篇的IPS計算為每月的IPS.

每篇的 IOS、IPS 如下檔案: 03featureExtraction_featureSelection/ios_ips.csv  
每上市公司的 IOS、IPS 位於: 04gettingTables\company_table

shengSheKe_chineseNewSentiment
==============================

1. 情緒辭典的選擇

有分為一般性情緒辭典(台大)跟金融類情緒辭典(廈門大學)


|    name    | source |weight|file position
| ---------- | --- |--------|------|
| 台湾大学简体中文情感极性词典ntusd |  https://reurl.cc/mdn94W |0.4|00ref/詞典|
| 中文財務情緒字典 |https://clip.csie.org/10K/publications |0.6|00ref/詞典/中文財務情緒字典|


2. 利用情緒辭典找出極端正負新聞的分數(搜集所有潛在的特徵詞)做為我們的標註依據

  1. 前5% (樂觀)：包括 03featureExtraction_featureSelection/pos_table.csv
  2. 後5% (悲觀)：包括 03featureExtraction_featureSelection/neg_table.csv
  3. 標註完成在: 03featureExtraction_featureSelection/labled_table.csv

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

# -*- coding: utf-8 -*-
import requests,logging
import time,datetime
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


prefix = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
# chromedriverの設定
options = Options()
options.add_argument('--headless')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
URL     = "https://www.google.com/search?q="

# loggerの設定
logger = logging.getLogger(__name__)
logging.basicConfig(filename="./logs/{0}_searcch.log".format(prefix),level=logging.INFO, format = "%(asctime)s %(levelname)s :%(message)s")

def get_total_result(keys):
    start_time = time.time()
    result = requests.get(URL+keys, headers=headers)    
    soup = BeautifulSoup(result.content, 'html.parser')   
    try:
        total_results_text = soup.find("div", {"id": "result-stats"}).find(text=True, recursive=False)
        results_num = ''.join([num for num in total_results_text if num.isdigit()])
        
        proc_time = time.time() - start_time
        
        if proc_time < 1:
            proc_time = 1
        else:
            proc_time = int(round(proc_time,0))        
        return results_num,proc_time
    except:
        return -1,10
    
def get_totalresults():
    #keywords.txt内に記載のキーボードのtotal_resultを連続的に取得する
    with open('keywords.txt',encoding='UTF-8') as f:
        keywords = f.readlines()
    
    for key in keywords:
        key = key.replace("\n","")
        total_result,proc_time = get_total_result(key)
        msg = "\t{0}\t{1}\t{2}".format(key,total_result,proc_time)
        print(msg)
        logger.info(msg)
        time.sleep(proc_time)
        
### Main ###
if __name__ == '__main__':
    get_totalresults()

#!/usr/bin/env python
# coding:utf8
# author:Z time:2018/4/20
#爬取酷狗TOP500并保存到MongoDB
import requests
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
import re
client = MongoClient()  # mongodb server
songs = client.kugou_db.songs # song collection
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}
def get_info(url):
    wb_data=requests.get(url,headers=headers)
    soup=BeautifulSoup(wb_data.text,'lxml')
    ranks=soup.select('.pc_temp_num')
    titles=re.findall('<a.*?class="pc_temp_songname".*?>(.*?)</a>',wb_data.text,re.S)
    song_times=soup.select('.pc_temp_time')

    for rank, title, song_time in zip(ranks, titles, song_times):
        data={
            'rank':rank.get_text().strip(),
            'singer':title.split('-')[0].strip(),#歌手
            # 'singer':title.get_text().split('-')[0].strip(),
            # 'song': title.get_text().split('-')[1].strip(),
            'song': title.split('-')[1].strip(),#歌曲名字
            'song_time':song_time.get_text().strip(),#歌曲时间
        }
        print(data)
        # exit()
        song_id=songs.insert(data)#插入文档到MongoDB
        print(song_id)#打印主键
if __name__ == '__main__':
    urls=['http://www.kugou.com/yy/rank/home/{}-8888.html?from=rank'.format(str(i)) for i in range(1,24)]
    for url in urls:
        get_info(url)
        time.sleep(1)#睡一秒防止爬取过快被封

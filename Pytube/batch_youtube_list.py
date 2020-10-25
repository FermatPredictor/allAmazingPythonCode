import os
from pytube import YouTube
import requests
import re
import time

"""
Notice:
本程式可能過一段時間就會失效，
需查看是否有最新版本更新
(2020/10/25: https://pypi.org/project/pytube4/)

目前的版本可能需要嘗試多次才能download 成功
"""

def download_play_list(url, path = None):
    """
    函數功能: 
    下載youtbute的playlist (參考用，目前本函數似乎不太好用)
    path: 下載影片路徑，未指定則載至當前資料夾
    """
    html = requests.get(url)
    res = re.findall(r'/watch[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', html.text)  #取得包含「/watch」的網址內容
    video_list = list(map(lambda x: 'https://www.youtube.com' + x, \
                      set(filter(lambda x: 'list=' in x and 'index=' in x, res))))
    download_list(video_list, path)


def download_list(url_list, path = None):
    """
    函數功能: 
    url_list是一個list，內含多個yt網址
    path: 下載影片路徑，未指定則載至當前資料夾
    """
    path = path or '.\\'
    if not os.path.isdir(path):  #防呆: 如果資料夾不存在就建立
        os.mkdir(path)
    for i, line in enumerate(url_list):
        try:
            yt = YouTube(line)
            print(f"{i}. {yt.title}")  #顯示標題
            yt.streams.get_highest_resolution().download(path)
        except Exception as e:
            print(e)
            print(f'第{i}個影片下載失敗')
        time.sleep(3) # 避免連續發太多request給線上


def download_by_txt(file, path = None):
    """
    函數功能: 
    下載檔案中的yt網址(以換行符號分隔)
    path: 下載影片路徑，未指定則載至當前資料夾
    caller example:
    download_by_txt('video.txt', path = r'.\music')
    """
    with open(file) as file:
        urls = file.readlines()
    download_list(urls, path)
        
if __name__ == "__main__":
    path = r'.\music'
    download_by_txt('video.txt', path = path)
    
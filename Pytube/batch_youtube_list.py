import os
from pytube import YouTube
from pytube import Playlist
import time

"""
當前版本: https://pypi.org/project/pytube/
pytube 10.0.0
"""

def download_play_list(url, path = None):
    """
    函數功能: 
    下載youtbute的playlist
    path: 下載影片路徑，未指定則載至當前資料夾
    """
    path = path or '.\\'
    if not os.path.isdir(path):  #防呆: 如果資料夾不存在就建立
        os.mkdir(path)
    pl = Playlist(url)
    for i, yt in enumerate(pl.videos):
        try:
            print(f"{i}. {yt.title}")  #顯示標題
            yt.streams.get_highest_resolution().download(path)
        except Exception as e:
            print(e)
            print(f'第{i}個影片下載失敗')


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
        time.sleep(2) # 避免連續發太多request給線上


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
    play_list_url = '' # enter yout url
    #download_by_txt('video.txt', path = path)
    download_play_list(play_list_url , path = path)

            
    
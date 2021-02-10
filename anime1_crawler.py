import os
from bs4 import BeautifulSoup
import urllib.request as req
import requests
import time
import re
from urllib.parse import unquote #解碼
import urllib3

headers = {
    "user-agent" : "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2825.67 Safari/537.36",
    "cookie" : "customLocale=zh_TW"
}
number = input('輸入號碼：')

url1 = 'https://anime1.me/'+ number 
print(url1)
request = req.Request(url1, headers=headers) #爬蟲part.1
with req.urlopen(request) as response:
    data = response.read().decode('utf-8')  
# print(data)

soup = BeautifulSoup(data,'html.parser')#'html.parser'為HTML的解析器
title = soup.find_all('h1',class_="entry-title")
file_name = title[0].text #取得檔名
print(file_name) 

frame = soup.find_all('iframe',class_="vframe")
frame_url = frame[0]['src'] #取得影片檔網址---(1)
print(frame_url)

website = requests.get(frame_url) #爬蟲part.2
regex = r"x\.send\(\\'d=(.*?)\\'" #取得FormData
origin = re.search(regex, str(website.content) ,re.M|re.I).group(1) #因為(.*?)只有一個 所以group為1

formData = { "d" : str(unquote(origin)) } #解碼FormData
videoAPI = requests.post('https://v.anime1.me/api', formData)
videoAPI = str(videoAPI.content)
# print(videoAPI)
posi = videoAPI.find('\\\\/\\\\/')
videoURL = videoAPI.replace(videoAPI[:posi + 6],'')
videoURL = videoURL.replace('\"}\'','')
videoURL = videoURL.replace('\\\\','')
videoURL = videoURL.replace('\\\\','') #取得影片檔網址---(2)
# print(videoURL)

file_path = 'D:\\Users\\Desktop' + '\\' + file_name[:-5]
if not os.path.exists(file_path):
    try:
        os.mkdir(file_path) #建立影片資料夾
    except:
        os.mkdir('D:\\Users\\Desktop' + '\\待命名')
        file_path =  'D:\\Users\\Desktop' + '\\待命名'

urllib3.disable_warnings()
print('準備下載影片...')
video_from = requests.get('https://' + videoURL,stream=True,verify=False) #從影片網址取得網頁資訊
print('已取得影片資訊...')
video = open(file_path + "\\" + file_name[-4:] + '.mp4', "wb+")  # 開啟資料夾及命名影音檔 # 寫入影音檔的二進位碼 
print('正在寫入影片資訊...')
video.write(video_from.content)
print('已完成!')
video.close()
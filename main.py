import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials 
import json
import time
from bs4 import BeautifulSoup

API_KEY=""

# 変数呼び出し
with open('.env') as f:
    API_KEY = f.read()

channelIdList = []
pageToken = ""

def main(pageToken, loopCount):
    response = getChannelTitle(pageToken)
    pageToken = response['nextPageToken']
    count = len(response['items'])
    channelId = ""
    channelUrl = ""

    for num in range(count):
        time.sleep(1)
        print("✅item数：" + str(len(response['items'])) + " num：" + str(num))
        channelId = response['items'][num]['snippet']['channelId']
        if channelId not in channelIdList:
            channelIdList.append(channelId)
            channelUrl = "https://www.youtube.com/channel/" + channelId
            channelName = response['items'][num]['snippet']['channelTitle']
            writeSheet(loopCount, channelName, channelUrl)
            loopCount += 1
    if loopCount < 400:
        main(pageToken, loopCount)

def getChannelTitle(pageToken):
    url = "https://www.googleapis.com/youtube/v3/search?type=video&part=snippet&maxResults=50&order=viewCount&key="
    keyword = "漫画動画"
    response = requests.get(url + API_KEY + "&q=" + keyword + "&pageToken=" + pageToken)

    print(response.json())
    return response.json()

def writeSheet(loopCount, channelName, channelUrl):
    scope = ['https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('scra-293404-c072c878c1d1.json', scope)
    gc = gspread.authorize(credentials)
    wks = gc.open('pythonで書き込みテスト').sheet1

    # チャンネル名書き込み
    wks.update_acell('A' + str(loopCount), channelName)
    print(wks.acell('A' + str(loopCount)))
    # チャンネルURL書き込み
    wks.update_acell('B' + str(loopCount), channelUrl)
    print(wks.acell('B' + str(loopCount)))

try:
    main(pageToken, 2)
except Exception as e:
    print(e)


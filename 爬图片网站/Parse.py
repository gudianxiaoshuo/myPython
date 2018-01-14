import requests
from bs4 import BeautifulSoup

import common

def FindAllTag(httpWeb,tag,tagClass):

    if common.BWebFile(httpWeb):
        html= requests.get(httpWeb).text
    else:
        html=common.readFile(httpWeb)

    htmlSp=BeautifulSoup(html,"html.parser")

    if tagClass:
        allNeedTag=htmlSp.find_all(tag,class_=tagClass)
    else:
        allNeedTag = htmlSp.find_all(tag)

    return allNeedTag

#获得tag下的所有<img>
def FindAllImg(httpWeb,tag,tagClass):
    allNeedTag=FindAllTag(httpWeb,tag,tagClass)
    imgList=[]
    for tag in allNeedTag:
        tagSp=BeautifulSoup(str(tag),"html.parser")
        imgList+=tagSp.find_all("img")

    return imgList
#!/usr/bin/env Python
#coding=utf-8

import jieba
import jieba.analyse
import jieba.posseg as psg
import common
import re
from zhon.hanzi import punctuation
import draw
from head import *

from wordcloud import WordCloud,ImageColorGenerator


import numpy as np #科学数值计算包，可用来存储和处理大型矩阵

from collections import Counter #专门计数问题的方法

from PIL import Image
import matplotlib.pyplot as plt  #数学绘图库

def GetBookTxt(bookPath):
    txt=common.GetFileContent(bookPath)
    return txt

def jiebaFenci(bookPath,stopPath):

    wList=GetCutWords(bookPath,stopPath,1)
    draw.ToWordCloud(wList,backImgPath,fontPath,300)

#根据词性分词
#bExtractKey False 根据词性进行分词
#            True  提取关键字的方式
def jiebaFenciByAtt(bookPath,stopPath=stopWordPath,att="n",num=100,bExtractKey=False):
    wList = GetCutWords(bookPath, stopPath, 1)
    str = "/".join(wList)
    if bExtractKey: #提取关键字方式
        keyDict=ExtractKeyWords_dict(str,num,("%s"%att,))
        draw.ToWordCloud_dict(keyDict,backImgPath,fontPath,num)
    else: #先普通分词，去除停用词，再词性分词

        wAttList=GetAtrributeWords(str,att)
        # GenerateCloudWord(wAttList, backImgPath,fontPath, 300)
        countdict= Counter(wAttList)
        draw.ToWordCloud_dict(countdict, backImgPath,fontPath, num)







def GetTop(wlist,num):
    countList=Counter(wlist)
    if num>len(countList):
        num=len(countList)

    return countList.most_common(num)

def GetBookTop(bookPath,num,att="",nMinLen=1,stopPath=stopWordPath):
    wList = GetCutWords(bookPath, stopPath, nMinLen)

    if att=="":
        return GetTop(wList,num)
    else:
        str = "/".join(wList)
        wAttList = GetAtrributeWords(str, att)
        return GetTop(wAttList, num)


# 统计列表中字符串 在str中出现的次数
def GetSubStrCount(str,subStrList):
    countList=map(lambda x:str.count(x),subStrList)
    return countList


#去除停用字
def CleanWords(wList,nMinLen=1,stopPath=stopWordPath):
    stopWords = common.GetStopWordsList(stopPath)
    wlist2=[]
    for cutWord in wList:
        w=cutWord.strip()
        w=re.sub("[%s\n-。]+" %punctuation, "", w) #去除标点符号
        w=re.sub("第?\w+[回|卷|章]","",w)
        if w.__len__()>=nMinLen and not common.BEng(w):
            if w not in stopWords:
                wlist2.append(w)
    #str="|".join(wlist2)        #转换成字符串

    return wlist2


#gensim所需的向量列表形式
def GetGensimList(filePath,att="",bAddTail=True):
    sentences=[]
    with open(filePath,"r",encoding="UTF-8") as f:
        subList=[]
        for line in f:
            if att=="":
                subList=list(jieba.cut(line.strip()))
            else:
                subList= list(psg.cut(line.strip()))

            if bAddTail:
                subList.append(line)
            sentences.append(subList)
    return sentences

#gensim列表 去除停用字
#gensim列表 中的 每一个元素又是一个列表，列表中是分词
def CleanWords_gensim(gensimwList,nMinLen=1,att="",stopPath=stopWordPath,bAddTail=True):
    stopWords = common.GetStopWordsList(stopPath)
    wlist2=[]

    for wList in gensimwList:

        if bAddTail:
            tailStr=wList[-1]
            del wList[-1]
        subList=[]
        for cutWord in wList:

            if isinstance(cutWord,str):
                w=cutWord.strip()
            else: # 词性分词
                slist=list(cutWord)
                w=slist[0]
                if len(slist)>1:
                    attribute=slist[1]
                if att!="" and att!=attribute:
                    continue

            w=re.sub("[%s\n-。\ufeff]+" %punctuation, "", w) #去除标点符号
            w=re.sub("第?\w+[回|卷|章]","",w)
            if w.__len__()>=nMinLen and not common.BEng(w):
                if w not in stopWords:
                    subList.append(w)
        if subList.__len__()>0:
            if bAddTail:
                subList.append(tailStr)
            wlist2.append(subList)

    return wlist2



#根据停用词，获得这本书的分词
def GetCutWords(bookPath,stopPath=stopWordPath,nMinLen=1):
    txt=GetBookTxt(bookPath)
    wList = list(jieba.cut(txt))  # 转换成列表
    wlist2=CleanWords(wList,nMinLen,stopPath)
    return wlist2

#获得某个词性的分词
def GetCutWords_Att(bookPath,att="n",stopPath=stopWordPath,nMinLen=1):
    wlist=GetCutWords(bookPath,stopPath,nMinLen)
    wAttList=GetAtrributeWords("/".join(wlist),att)
    return wAttList


#词性分词
def GetAtrributeWords(str,att):
    wList = list(psg.cut(str))  # 词性分词，速度慢，可以先普通分词，去停用词后，在词性分词

    wlist2=[]

    for cutWord in wList:
        if cutWord.flag==att:
            wlist2.append(cutWord.word)

    return wlist2

#根据词性 提取关键字
def ExtractKeyWords_dict(str,maxKeynum,attrTuple):

    tags=jieba.analyse.extract_tags(str,maxKeynum,allowPOS=attrTuple,withWeight=True)
    keywords=dict()
    for i in tags:
        keywords[i[0]]=i[1] # i[0]-- 关键词   i[1]--权重

    return keywords




def init():
    jieba.load_userdict(dictPath)





#jiebaFenci("红楼梦.txt",stopWordPath)
#jiebaFenciByAtt("西游记.txt",stopWordPath,"ns",100,True)




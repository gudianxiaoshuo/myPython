#!/usr/bin/env Python
#coding=utf-8
import jieba
import common
from head import *
import dataParse

import pickle

from gensim import corpora, models, similarities

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



def GenList(filePath,att="",bAddTail=False):
    dataParse.init()
    sentences = dataParse.GetGensimList(filePath, att,bAddTail=bAddTail)
    genList = dataParse.CleanWords_gensim(sentences, nMinLen=1, att=att,bAddTail=bAddTail)
    return genList



#生成字典
def GenDic(filePath,att="",savePath=""):
    genList = GenList(filePath,att=att)
    dictionary = corpora.Dictionary(genList)
    if savePath!="":
        dictionary.save(savePath)
    return dictionary

#生成字典
def GenDic_byList(genList,savePath=""):
    dictionary = corpora.Dictionary(genList)
    if savePath!="":
        dictionary.save(savePath)
    return dictionary


#用字典将语料词袋转换为向量空间
def GenList2Bow(genList,dic,savePath=""):
    corpus=[dic.doc2bow(subtextList) for subtextList in genList]
    if savePath!="":
        corpora.MmCorpus.serialize(savePath,corpus)
    return corpus

#初始语料转换为tfidf语料
def OriCorpus2tfidf(corpus,savePath=""):
    tfidf_model = models.TfidfModel(corpus)
    corpus_tfidf=tfidf_model[corpus]

    if savePath:
        corpora.MmCorpus.serialize(savePath, corpus_tfidf)

    return corpus_tfidf

#tfidf语料，编制成索引
def ToIndex(corpus_tfidf,savePath=""):
    index=similarities.MatrixSimilarity(corpus_tfidf)

    if savePath:
        index.save(savePath)
    return index


class MyCorpus(object):
    def __init__(self,dic,filePath):
        self.dic=dic
        self.filePath=filePath

    def __iter__(self):
        for line in open(self.filePath,"r",encoding="utf-8"):
            line=line.strip()
            if line=="":
                continue
            wList=jieba.cut(line)
            yield self.dic.doc2bow(wList)

#将本地文件，转换为向量空间
def ToBow(dic,filePath,savePath=""):
    '''

    :param dic:       字典
    :param filePath:
    :return:          向量
    '''
    corpus_mem_friendly=MyCorpus(dic,filePath)
    vec=[]
    for lineVec in corpus_mem_friendly:
        if lineVec: #非空向量加入，       空向量则略去
            vec.append(lineVec)

    if savePath:
        corpora.MmCorpus.serialize(savePath, vec)  # store to disk, for later use
    return vec


def SaveVec(vec,savePath):
    if savePath:
        corpora.MmCorpus.serialize(savePath, vec)  # store to disk, for later use

#预处理阶段，生成并保存各种信息
def SaveRc(filePath,bookName,dirPath=""):

    #生成字典
    dic=GenDic(filePath)
    if dirPath:
        prePath="/".join([dirPath,bookName])
    else:
        prePath=bookName

    #保存字典
    dicPath=".".join([prePath,"dict"])
    dic.save(dicPath)                                      # 字典 dict

    genList=GenList(filePath,bAddTail=True)

    #文档（段落）索引对应关系
    docMapPath=".".join([prePath, "pkl"]) #文档映射，这里是段落映射
    docDict={}
    nIndex=0
    for li in genList:
        doc=li[-1]
        docDict[nIndex]=doc
        del li[-1]
        nIndex+=1

    output=open(docMapPath,"wb")
    pickle.dump(docDict,output)        # 保存  文档索引
    output.close()

    #初始语料
    corpus=GenList2Bow(genList,dic)
    #模型
    tfidf_model = models.TfidfModel(corpus)
    #tf语料
    corpus_tfidf=tfidf_model[corpus]
    #保存语料
    bowPath_tfd = ".".join([prePath, "mm_tf"])
    corpora.MmCorpus.serialize(bowPath_tfd, corpus_tfidf) # tfidf语料

    #保存模型
    tf_modelPath = ".".join([prePath, "tfidf"])
    tfidf_model.save(tf_modelPath)                         # tfidf模型

    #lsi模型，及lsi语料
    lsi_model = models.LsiModel(corpus_tfidf, id2word=dic, num_topics=200)
    corpus_lsi = lsi_model[corpus_tfidf]

    #保存lsi语料
    bowPath_lsi= ".".join([prePath, "mm_lsi"])
    corpora.MmCorpus.serialize(bowPath_lsi, corpus_lsi)    #lsi 语料

    #保存lsi模型
    lsi_modelPath = ".".join([prePath, "lsi"])
    lsi_model.save(lsi_modelPath)     #lsi模型     same for tfidf, lda, ...

    Word2Vec(genList, ".".join([prePath, "w2v"]))


    #将lsi语料编制成索引形式，方便查询，并保存
    simIndex = similarities.MatrixSimilarity(corpus_lsi)  #编制索引
    indexPath=".".join([prePath, "index"])
    simIndex.save(indexPath)


#加载各种信息
def LoadRc(bookName,dirPath=""):
    if dirPath:
        prePath="/".join([dirPath,bookName])
    else:
        prePath=bookName
    #加载文档索引的字典对应关系
    pklfile=open(".".join([prePath,"pkl"]),"rb")
    docDict=pickle.load(pklfile)
    pklfile.close()
    #加载字典
    dic = corpora.Dictionary.load(".".join([prePath,"dict"]))
    #加载tfidf语料
    corpus_tf = corpora.MmCorpus(".".join([prePath,"mm_tf"]))
    #加载lsi语料
    corpus_lsi = corpora.MmCorpus(".".join([prePath, "mm_lsi"]))
    #加载tfidf模型
    tf_model = models.TfidfModel.load(".".join([prePath, "tfidf"]))
    #加载lsi模型
    lsi_model = models.LsiModel.load(".".join([prePath, "lsi"]))

    #加载语料编制的索引文件
    simIndex = similarities.MatrixSimilarity.load(".".join([prePath, "index"]))

    return dic,corpus_tf,corpus_lsi,tf_model,lsi_model,docDict,simIndex

#查询相近性
def Qurey(qStr,dic,tfidf_model,lsi_model,simIndex,docDict):

    #查询字符串转初始语料
    bow=dic.doc2bow(jieba.cut(qStr))
    #初始语料转tfidf语料
    tfidf_bow=tfidf_model[bow]
    #tfidf语料转lsi语料
    lsi_bow=lsi_model[tfidf_bow]
    #计算查询语料在语料索引空间中相近度
    sim_q=simIndex[lsi_bow]
    #按相近度进行排名
    sims = sorted(enumerate(sim_q), key=lambda item: -item[1])
    for k, v in sims[:50]:
        print(k, v, docDict[k])


def QureyStr(qStr,bNeedSave=False):

    if bNeedSave:
        # 初始化
        # 红楼梦字典生成、语料生成、模型生成、索引生成，文档对应关系，并保存起来
        SaveRc("红楼梦.txt","红楼梦","tmp")

    # 加载字典、语料、模型、索引、文档对应关系
    dic, corpus_tf, corpus_lsi, tf_model, lsi_model, docDict, simIndex = LoadRc("红楼梦", "tmp")

    # 在小说中 查询与这一句话，最相近的段落
    Qurey(qStr, dic, tf_model, lsi_model, simIndex, docDict)



def Word2Vec(simList,savePath=""):
    model=models.Word2Vec(simList,       #gensim 列表形式的语句
                            size=100,    #词向量维度
                            window=5,
                            min_count=5, #只考虑出现次数大于5的词
                            workers=4)

    if savePath:
        model.save(savePath)

    return model

def QureyWord(qWord):
    model=models.Word2Vec.load("tmp//红楼梦.w2v")
    for k,v in model.most_similar(positive=[qWord]):
        print(k,v)

#find_relationship("宝玉","黛玉","宝玉")
def find_relationship(a, b, c):
    """
    返回 d
    a与b的关系，跟c与d的关系一样
    """
    model = models.Word2Vec.load("tmp//红楼梦.w2v")
    d, _ = model.most_similar(positive=[c, b], negative=[a])[0]
    print("给定“{}”与“{}”，“{}”和“{}”有类似的关系".format(a, b, c, d))

# SaveRc("红楼梦.txt","红楼梦","tmp")
# QureyWord("凤姐")
find_relationship("宝玉","黛玉","宝玉")

import dataParse
import draw
import MLearn


def sample1():
    dataParse.init()
    #提取关键字的形式分词，并生成词云
    dataParse.jiebaFenciByAtt("西游记.txt",att="nr",num=100,bExtractKey=True)



def sample2():
    #根据词性 分词，生成词云
    dataParse.init()
    wlist=dataParse.GetCutWords_Att("西游记.txt","ns")
    draw.ToWordCloud(wlist)


def sample3():
    dataParse.init()
    # 获得出现次数最多的前20个分词  每个分词 词性是 n  最小长度是 2
    topList = dataParse.GetBookTop("西游记.txt", 20, "n", 2)

    # 生成条状图
    draw.barh_dict(topList)
    # 生成词云
    draw.ToWordCloud_dict(dict(topList))


def QureyStr(qStr):
    MLearn.QureyStr(qStr)


sample3()
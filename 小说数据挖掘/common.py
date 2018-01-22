
import regex
import re
import jieba
import jieba.posseg as psg

def write(path,linkList,openStyle="w"):
    if isinstance(linkList,list) or isinstance(linkList,set):
        with open(path,openStyle,encoding="utf-8") as f:
            for each in linkList:
                f.write(each+"\n")

    if isinstance(linkList,str):
        with open(path, openStyle, encoding="utf-8") as f:
            f.write(linkList)



def GetStopWordsList(filePath):
    #stopWords=[line.strip() for line in open(filePath,"r",encoding="utf-8").readlines()]
    stopWords=[]
    for line in open(filePath,"r",encoding="utf-8").readlines():
        unicodeHead="\ufeff"     #unicode文件头
        line=line.strip("\r\n %s"%unicodeHead)
        stopWords.append(line)
    return stopWords



def GetFileContent(filePath):
    with open(filePath,"r",encoding="utf-8") as f:
        return f.read()
    return ""










def ReadFileList(filePath):
    List=[]
    with open(filePath, "r", encoding="UTF-8") as f:
        for line in f:
            line = line.strip("\n ")  # 'https://flowerillust.com/frame.html\n'  去掉换行符
            List.append(line)
    return List


def BBiaodian(str):
    re = regex.compile(r"^[-！？｡＂＃＄％＆＇（）＊＋，－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’‛“”„‟…‧﹏.]+$")
    bMatch = re.match(str)
    if bMatch:
        return True
    else:
        return False


def BEng(str):

    re=regex.compile(r"^[A-Za-z0-9]+$")
    bMatch=re.match(str)
    if bMatch:
        return True
    else:
        return False



def GetTop(n,wlist):
    if n>len(wlist):
        n=len(wlist)

    keys = set(wlist)
    dic = {}
    for w in keys:
        dic[w] = wlist.count(w)

    dlist = list(dic.items())
    dlist.sort(key=lambda x: x[1], reverse=True)

    relist=[]
    for i in range(20):
        relist.append(i)

    return relist


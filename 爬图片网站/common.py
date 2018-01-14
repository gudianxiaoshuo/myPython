from down import downHtml,bExist,downImg
import requests
from bs4 import BeautifulSoup

from tld import get_tld
import os
import glob

import Parse
import down



'''
防止出现http连接太多没有关闭的错误
Max retries exceeded with url:
'''

requests.adapters.DEFAULT_RETRIES = 5 #尝试链接次数
s = requests.session()
s.keep_alive = False





def GetLastName(str):
    nIndex=str.rfind("/")
    nDot=str.rfind(".")
    if nIndex>=0 and nDot>=0:
        subStr=str[nIndex+1:nDot]
        temp=subStr
        return subStr
    return ""

#https://flowerillust.com/
#flowerillust.com
def GetDomain(urlStr):
    host = get_tld(urlStr)
    return host



def GetHttpDomain(urlStr):
    host=get_tld(urlStr)
    url=urlStr.lower()
    pre=""
    if url.startswith("http://"):
        pre="http://"
    elif url.startswith("https://"):
        pre="https://"

    return pre+host+"/"






def write(path,linkList,openStyle="w"):
    if isinstance(linkList,list) or isinstance(linkList,set):
        with open(path,openStyle,encoding="utf-8") as f:
            for each in linkList:
                f.write(each+"\n")

    if isinstance(linkList,str):
        with open(path, openStyle, encoding="utf-8") as f:
            f.write(linkList)


def readFile(filePath):
    with open(filePath,"r",encoding="utf-8") as f:
        return f.read()
    return ""

#读取文件，将链接保存在列表中
#读取文件

'''
linkList.clear()
print("读取文件内容,并放入列表中")
common.readLinkFile(filePath,linkList)
'''
def readLinkFile(filePath,List):
    with open(filePath) as f:
        for line in f:
            line = line.strip("\n")  # 'https://flowerillust.com/frame.html\n'  去掉换行符
            List.append(line)




#下载所有列表中的链接，以链接的最后的字段作为名字
#并将其保存在dir目录中
def downAlllinks(linkList,dir):
    '''

    :param linkList: 待下载的网址列表
    :param dir:      保存的本地目录
    :return:
    '''
    nIndex=0
    html = ""
    for subLink in linkList:
        print("正在下载%d" % (nIndex))
        html = downHtml(subLink, "shift_jis")
        print("已经获取%d" % (nIndex))
        subParse = BeautifulSoup(html, "html.parser")
        tempName = GetLastName(str(subLink))
        print(tempName)
        tempFile = dir + tempName + ".txt"
        write(tempFile, str(subParse.prettify()))
        nIndex += 1

#如果链接对应的本地文件不存在，则下载，并将其保存在dir目录中
#若存在，则跳过，不下载
def downAllLinksIfNotExists(allLinks,dir):
    nIndex = 0
    for subLink in allLinks:
        print("正在下载%d" % (nIndex))
        tempName = GetLastName(str(subLink))
        tempFile = dir+ tempName + ".txt"
        if os.path.exists(tempFile):
            print("以存在%s" % (tempName))
            nIndex += 1
            continue

        html =downHtml(subLink, "shift_jis")
        print("已经获取%d" % (nIndex))

        subParse = BeautifulSoup(html, "html.parser")

        print("正在保存 %s" %(tempName))
        write(tempFile, str(subParse.prettify()))
        nIndex += 1


#查找标签
def FindAllTag(httpWeb,tag,tagClass):
    '''

    :param httpWeb:   如果是网页形式，则下载网页，否则读取本地文件
    :param tag:
    :param tagClass:
    :return:    查找到的标签列表
    '''

    #网页
    if httpWeb.find("http://")!=-1 or httpWeb.find("https://")!=-1:
        html = downHtml(httpWeb)
    else:
    #读取本地文件
        html = readFile(httpWeb)

    htmlSp = BeautifulSoup(html, "html.parser")
    if tagClass:
        allNeedTag=htmlSp.find_all(tag,class_=tagClass)
    else:
        allNeedTag = htmlSp.find_all(tag)
    return allNeedTag

def FindAllHref(httpWeb,tag,tagClass):
    allNeedTag = FindAllTag(httpWeb, tag, tagClass)
    allLinks=[]
    for div in allNeedTag:
       divSp = BeautifulSoup(str(div), "html.parser")
       a = divSp.find("a")
       if a and a.get("href"):
           allLinks.append(a.get("href"))

    return allLinks

#获得tag标签下img的链接
def FindAllImg(httpWeb,tag,tagClass,srcValue="src"):
    '''

    :param httpWeb:
    :param tag:        标签    如 div
    :param tagClass:   标签类  如 class
    :param srcValue:   查找的img标签的 某个属性
    :return:           返回，查到到的图片链接列表
    '''
    allNeedTag = FindAllTag(httpWeb, tag, tagClass)
    allLinks=[]
    for div in allNeedTag:
       divSp = BeautifulSoup(str(div), "html.parser")
       a = divSp.find("img")
       if a and a.get(srcValue):
           allLinks.append(a.get(srcValue))

    return allLinks


# 根据主网址，获得所有分页网址，将它们一起放入allLinks中
# 根据主网址
# 获得所有主网址的分页网址
# 主网址对应的网页内容，保存在本地dir中
# 分页网址 在网页源码中 位于  class=tagclass 的  tag 标签下的<a  href>下
# 将主网址和分页网址，保存在allLink列表中

def GetAllPages(mainLink,allLinks,dir,tag,tagclass):
    '''

    :param mainLink: 主链接网址列表
    :param allLinks: 主链接以及获得的分页链接，都保存在这个列表中
    :param dir:      主链接对应的网页，保存在本地目录中
    :param tag:      分页链接，对应的tag标签
    :param tagclass: 分页链接，对应的tag的class
    :return:
    '''
    for subLink in mainLink:
        allLinks.append(subLink)
        domain=GetHttpDomain(subLink)
        tempName = GetLastName(str(subLink))
        filePath = dir+ tempName + ".txt"
        divs = FindAllTag(filePath, tag, tagclass) # divs=common.FindAllTag(subLink,"div","link2")

        for div in divs:
            divSp = BeautifulSoup(str(div), "html.parser")
            a = divSp.find("a")
            if a and a.get("href"):
                allLinks.append(domain + a.get("href"))
    return 1


# 分页链接这种形式 <a href="cat-aliens-and-extraterrestrials-33.htm?page=2">
# 下载所有分页链接  下载到目录dir下
def GetAllPages(domain,txtFile,aTagList,dir,tag,tagclass):
    '''

    :param txtFile:  主分类网址文件
    :param aTagList: 主链接以及获得的分页链接，都保存在这个列表中
    :param dir:      本地目录
    :param tag:      分页链接，对应的tag标签
    :param tagclass: 分页链接，对应的tag的class
    :return:
    '''
    bExist = ParseInit(txtFile, aTagList, dir, tag, tagclass)
    if not bExist:
        return False

    if len(aTagList) > 0:
        aTag = aTagList[-1]
        aLastHref = aTag["href"]
        pageHead = aLastHref.split("=")[0]
        nLastPage = int(aLastHref.split("=")[-1])
        for nIndex in range(2, nLastPage + 1):  # [2,nLastPage]
            page = domain + pageHead + "=%d" % nIndex
            DownAndSave(page, dir, str(nIndex))
    return True


# 获得所有分页
# 每个目录下，或者无子目录   存放着分页的第一个网址 解析此网址
#            或者有子目录    存放着更细的分类
def GetAllPagesEx(domain,maindir):
    '''
    分页网址的第一页文件，保存在最底层目录下，父亲目录都是类别信息
    :param domain:  主网站域名
    :param maindir: 主目录
    :return:        遍历主目录，根据主目录下保存的文件，下载所有的分页文件
    '''
    print(maindir)
    dirList = []
    GetAllSubDirs(maindir, dirList)  # 主分类目录

    if len(dirList)==0: #无子目录，则根据第一个分页，获得所有分页信息
        txtfileList = []
        GetAllSubFile(maindir, txtfileList, "txt")
        if len(txtfileList):
            txtFile = FindFirstPage(txtfileList)
            aTagList = []
            GetAllPages(domain, txtFile, aTagList, maindir, "ul", "pagination")
        return

    for subdir in dirList: #有子目录，则进入子目录，进一步遍历
        GetAllPagesEx(domain, subdir)

#解析txt本地分页文件，获得所需img标签，下载img
def DownImg(domain,dir,txt,tag,tagClass):
    html=readFile(txt)
    imgLinkList=Parse.FindAllImg(txt,tag,tagClass)
    down.MultiDownImg(domain,imgLinkList,dir)

    '''
      for img in imgLinkList:
        imglink=domain+img["src"]
        imgName = imglink.split("/")[-1]
        print(dir + "\\"+imgName)
        down.downImg(imglink, dir + "\\"+imgName)  
    '''





#下载分页网址中，指定标签下的img
def GetAllImg(domain,maindir,tag,tagClass):
    dirList=[]
    GetAllSubDirs(maindir, dirList)  # 主分类目录
    if len(dirList)==0: #无子目录，则此目录下所有txt文件为 分页文件
        txtfileList = []
        GetAllSubFile(maindir, txtfileList, "txt")

        for txt in txtfileList:
            DownImg(domain,maindir,txt,tag,tagClass)

    else: #有自目录，则递归调用
        for subdir in dirList: #有子目录，则进入子目录，进一步遍历
            GetAllImg(domain, subdir,tag,tagClass)










# 找到首页
# 首页用的网页作为名字 .htm.txt or .html.txt
# 其它分页用的数字作为名字
def FindFirstPage(txtfileList):

    nLen=len(txtfileList)
    if nLen<0:
        return ""

    if len(txtfileList)==1:
        return txtfileList[0]

    for name in txtfileList:
        if name.find("htm")!=-1:
            return name

    return txtfileList[0]


#是网络文件，还是本地文件
def BWebFile(domain):
    bWebFile = domain.find("http://") != -1 or domain.find("https://") != -1
    return bWebFile

def DownAndSave(domain,dir,fileName=""):
    #html=downHtml(domain,"shift_jis")
    bWebFile=BWebFile(domain)

    if bWebFile: #网址
        html = downHtml(domain)

        if fileName=="":
            name = domain.split("/")[-1]  # host=GetDomain(domain)
            name = name + ".txt"
        else:
            fileName=fileName.rstrip(".txt")
            name=fileName+ ".txt"

        htmlParse = BeautifulSoup(html, "html.parser")
        write(os.path.join(dir,name), htmlParse.prettify())  # 标准化输出
    else:
        html=readFile(domain) #本地文件

    htmlParse = BeautifulSoup(html, "html.parser")

    return htmlParse

#每个网站的初始化都不同，需分析
def ParseInit(domain,linkList,valueList,dir,tag,tagClass,aClass=""):
    '''

    :param domain:    分析的网址
    :param linkList:  a标签所需的 链接列表
    :param valueList: a标签所对应的值列表
    :param dir:       目录
    :param tag:       查找的标签Parent
    :param tagClass:  查找的标签类
    :param aClass:    标签Parent下 class=aClass的 a链接
    :return:
    '''
    htmlParse=DownAndSave(domain,dir)

    #找到menu菜单
    div_lists=htmlParse.find_all(tag, class_=tagClass)


    for div in div_lists:
        a_linkSoup=BeautifulSoup(str(div),"html.parser")
        if aClass=="":
            a_link=a_linkSoup.find_all("a")
        else:
            a_link = a_linkSoup.find_all("a", class_=aClass)

        for each in a_link:
            if each.get("href"):
                linkList.append(domain + each["href"])
                valueList.append(each.string)

    return 1

#递归分析网址，创建类别
#依据，主类别 次类别 所用的div的类都相同
'''
本例子中，主类别是下面这种形式，主类别
         <div class="cat">
         <a class="sidebar-letter" href="./cat-a-1.htm">
           A
         </a>         
A分类下的，次分类，也是这种形式          
< divclass ="cat" >
< aclass ="sidebar-letter" href="./cat-accordions-1769.htm" > Accordions</a>

'''
def ParseDomain(domain,dir,tag,tagClass,aClass=""):
    fileName = "html.txt"
    DownAndSave(domain, dir, fileName)
    filePath=os.path.join(dir,fileName)
    aList = []
    ParseInit(filePath, aList, dir, tag, tagClass, aClass)
    if len(aList)==0:
        return
    for v in aList:
        vStr=v.string.strip(" \n")
        subDir = dir + vStr + "\\";
        if not os.path.exists(subDir):
            os.makedirs(subDir)
        ParseDomain(domain + v["href"].lstrip("./"), subDir, tag, tagClass, aClass)





#每个网站的初始化都不同，需分析
def ParseInit(domain,aList,dir,tag,tagClass,aClass=""):
    '''

    :param domain:    分析的网址
    :param aList:     <a>标签对象
    :param dir:       目录
    :param tag:       查找的标签Parent
    :param tagClass:  查找的标签类
    :param aClass:    标签Parent下 class=aClass的 a链接
    :return:
    '''
    htmlParse = DownAndSave(domain, dir)

    #找到menu菜单
    div_lists=htmlParse.find_all(tag, class_=tagClass)
    #print(div_menu)

    if len(div_lists)==0:
        return False

    for div in div_lists:
        a_linkSoup=BeautifulSoup(str(div),"html.parser")
        if aClass=="":
            a_link=a_linkSoup.find_all("a")
        else:
            a_link = a_linkSoup.find_all("a", class_=aClass)

        for each in a_link:
            aList.append(each)

    return True



#目录下的文件和文件夹
def GetAllSubFile(dir,list):
    if os.path.exists(dir):
        files=os.listdir(dir)
        for file in files:
            fullPath=os.path.join(dir,file)
            list.append(fullPath)

#目录下的文件
def GetAllSubFile(dir,list,ext):
    if os.path.exists(dir):
        files=glob.glob(dir+"\\*.%s" %(ext))
        for file in files:
            list.append(file)

#目录下的文件夹
def GetAllSubDirs(dir,list):
    if os.path.exists(dir):
        files=os.listdir(dir)
        for file in files:
            fullPath=os.path.join(dir,file)
            if os.path.isdir(fullPath):
                list.append(fullPath)
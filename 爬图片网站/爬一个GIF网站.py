import common
import os
from bs4 import BeautifulSoup
import down

#创建目录
tmpDir="gif\\"
if not os.path.exists(tmpDir):
    os.makedirs(tmpDir)


#下载网站
domain=""


aList=[]



'''
linkList=[]  #   a标签所需的 链接列表
valueList=[] #   a标签所对应的值列表
common.ParseInit(domain,linkList,valueList,tmpDir,"div","cat","sidebar-letter")
print(linkList)
print(valueList)
for v in valueList:
    subDir=tmpDir+v;
    print(subDir)
    if not os.path.exists(subDir):
        os.makedirs(subDir)

'''
'''
common.ParseInit(domain,aList,tmpDir,"div","cat","sidebar-letter")
#print(aList)
#创建主目录

for v in aList:
    subDir=tmpDir+v.string+"\\";
    print(subDir)
    if not os.path.exists(subDir):
        os.makedirs(subDir)

    common.DownAndSave(domain+v["href"].lstrip("./"),subDir)



#创建子目录
subDirList=[]
common.GetAllSubDirs(tmpDir,subDirList)
print(subDirList)
print("------------- ----------------")
for subDir in subDirList:
    txtList=[]
    common.GetAllSubFile(subDir,txtList,"txt")
    print(txtList)

    aTagList=[]
    common.ParseInit(txtList[0],aTagList,subDir,"div","cat","sidebar-letter")

    for v in aTagList:
        vStr=v.string.strip(" \n")
        subsubDir = subDir+"\\" + vStr + "\\";
        print(subsubDir)
        if not os.path.exists(subsubDir):
            os.makedirs(subsubDir)

        common.DownAndSave(domain + v["href"].lstrip("./"), subsubDir)
        
        #根据图片首页链接，获得所有分页链接

subDirList=[]
common.GetAllSubDirs(tmpDir,subDirList) #主分类目录



        
        

'''
#创建类别
#common.ParseDomain(domain,tmpDir,"div","cat","sidebar-letter")
#获得所有分页
#common.GetAllPagesEx(domain,tmpDir)

common.GetAllImg(domain,tmpDir,"div","categories-outer")









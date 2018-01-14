import os
import common
import string
import MyThread
from time import sleep
import requests
from urllib import request
import urllib

import socket  #
socket.setdefaulttimeout(10.0)   #设置全局的socket超时
import ssl
ssl._create_default_https_context = ssl._create_unverified_context



def downHtml(http,encodeStr="utf-8"):
    '''
    下载网址 ，获得HTML内容
    :param http:      网址
    :param encodeStr: 网址编码
    :return html:     返回获得的网址内容
    '''
    html = ""
    while html=="":
        try:
            re= requests.get(http,timeout=3)
            re.encoding = encodeStr    #直接从原网页获得编码信息  或者# re.encoding = re.apparent_encoding 这种方式自动分析，占用时间可能长
            html=re.text
        except:                          #请求不成功的话，循环 但sleep一段时间，保持频率不要太高，以免被拒绝
            sleep(5)
            continue
    return html

def bExist(httpPath):

    bExist=True
    while bExist:
        try:
           request.urlopen(httpPath, timeout=10)
           break
        except urllib.error.HTTPError as e:
            if e.code==404:
                bExist = False
        except urllib.error.URLError as e:
            print(e.reason)
        except socket.timeout as e:
            print(e)
    return bExist

    # request.urlretrieve(httpPath,localPath)  直接下载 出现10060错误
    # requests.get('https://www.zhihu.com/',verify=False)  verify=False 要不然会有SSL错误
def downImg(httpPath,localPath):
    html = ""
    num=0
    nImgType=0 #先尝试PNG，再尝试JPG
    while html=="":
         try:
             num+=1
             if num>1:
                print("--第%d次尝试--" %num)

             headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"}

             req=request.Request(url=httpPath, headers=headers)
             #resp = request.urlopen(httpPath,timeout=60,headers=headers)
             resp = request.urlopen(req, timeout=60)
             html = resp.read()

         except urllib.error.HTTPError as e:
             if e.code==404:
                nImgType+=1
                httpPath='.'.join(httpPath.split(".")[0:-1])+".jpg"
                localPath=localPath.split(".")[0]+".jpg"
                if nImgType>=2:
                    return False #不存在
                else:
                    continue
         except (urllib.error.URLError, socket.timeout,Exception)as e:
             print(e)
             if num>50:
                 return False
             sleep(5)
             continue

    picFile = open(localPath, "wb")
    picFile.write(html)
    picFile.close()
    return True

#下载图片
def DownImg(domain,subDirList,subsubImgDir):
    '''
    :param subDirList:    文件夹列表
    :param subsubImgDir:  新创建的子文件夹，用以保存图像
    :return:
    '''
    for dir in subDirList:
        print("-------%s------" %dir)
        imgList=[]
        common.readLinkFile(dir+"\\img.txt",imgList)

        if not os.path.exists(dir + "\\%s\\"%subsubImgDir):
            os.makedirs(dir + "\\%s\\"%subsubImgDir)
        for img in imgList:
            imgName=img.split("/")[-1]
            print(imgName)
            common.downImg(domain+img,dir+"\\%s\\%s" %(subsubImgDir,imgName))



def GetRealImg(oriImg,ext=".png"):
    # img/flower2/s-flower5526.jpg
    # img/flower/flower5526.png
    splitlist = oriImg.split("/")
    s1=splitlist[0]                        # img
    s2=splitlist[1].rstrip(string.digits)  # flower
    s3=splitlist[2]                        # s-flower5526.jpg
    s3list=s3.split(".")
    s3=s3list[0]                           # s-flower5526
    subSplitList=s3.split("-")
    stemp="-".join(subSplitList[1:])        #flower5526
    return s1+"/"+s2+"/"+stemp+ext


#将图片链接，重新解析为新的链接地址，下载这个图片
def DownImgP(domain,subDirList,subsubImgDir,bParse=False):
    for dir in subDirList:
        print("-------%s------" %dir)
        imgList=[]
        common.readLinkFile(dir+"\\img.txt",imgList)

        if not os.path.exists(dir + "\\%s\\"%subsubImgDir):
            os.makedirs(dir + "\\%s\\"%subsubImgDir)
        for img in imgList:
            if bParse:
                img=GetRealImg(img,".png")
            name=img.split("/")[-1]
            print(name)
            common.downImg(domain+img,dir+"\\%s\\%s" %(subsubImgDir,name))





#多线程方式下载
def MultiDownImgP(domain,subDirList,subsubImgDir,bParse=False):

    mth=MyThread.CMultiDownThread(10)

    for dir in subDirList:
        print("-------%s------" %dir)
        imgList=[]
        common.readLinkFile(dir+"\\img.txt",imgList)

        if not os.path.exists(dir + "\\%s\\"%subsubImgDir):
            os.makedirs(dir + "\\%s\\"%subsubImgDir)
        for img in imgList:
            if bParse:
                img=GetRealImg(img,".png")
            name=img.split("/")[-1]
            print(name)
            th=MyThread.CDownThread(domain+img,dir+"\\%s\\%s" %(subsubImgDir,name))
            while not mth.AddThread(th):
                sleep(5)
    mth.join()

#多线程方式下载
def MultiDownImg(domain,imgLinkList,dir):

    mth=MyThread.CMultiDownThread(10)

    for img in imgLinkList:
        imglink=domain+img["src"]
        imgName = imglink.split("/")[-1]

        imgPath=dir + "\\"+imgName
        print(imgPath)

        th = MyThread.CDownThread(imglink, imgPath)
        while not mth.AddThread(th):
            sleep(5)

    mth.join()

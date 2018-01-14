import common
import os
import down




#创建目录
tmpDir="tmp\\"
if not os.path.exists(tmpDir+"htmls\\"):
    os.makedirs(tmpDir+"htmls\\")


domain="https://flowerillust.com/"

''' 
linkList=[] #创建空列表
valueList=[]
common.ParseInit(domain,linkList,valueList,tmpDir,"div","menu")


#将所有链接保存在文件中
filePath=tmpDir+"mainLinks.txt"
common.write(filePath,linkList)


'''
#下载链接，获得网页，将其保存到本地文件中
'''
common.downAlllinks(linkList,tmpDir+"htmls\\")

#通过主链接，解析获得
#获得所有分页链接网址
#连同主链接 一同保存在allLinks中
allPages=list()
common.GetAllPages(linkList,allPages,tmpDir +"htmls\\","div","link2")

common.write(tmpDir+"alllinks.txt",allPages)



common.downAllLinksIfNotExists(allPages,tmpDir+"htmls\\")


'''
#遍历目录下的本地网页，获得所有图片资源链接地址，将图片路径保存在img.txt中
'''


txtFileList=[]
common.GetAllSubFile(tmpDir+"htmls\\",txtFileList,"txt")

print(len(txtFileList))
preDir=""
num=0
for txtFile in txtFileList:
    txtDir=txtFile.rstrip(".txt")
    txtDir=txtDir.rstrip(string.digits)

    if preDir!=txtDir:
        if os.path.exists(txtDir+"\\img.txt"):
            os.remove(txtDir+"\\img.txt")
        num = 0
        preDir=txtDir

    if not os.path.exists(txtDir):
        os.makedirs(txtDir)

    print(txtDir)
    print(txtFile)
    hrefList=common.FindAllImg(txtFile,"div","subcontents","data-layzr")
    common.write(txtDir+"\\img.txt",hrefList,"a")
    num+=len(hrefList)
    common.write(txtDir + "\\num.txt", str(num))

M
'''

'''
IMG链接保存在子菜单下的img.txt中，
遍历所有子菜单，根据子菜单下的链接信息，下载图片，
'''
subDirList=[]
common.GetAllSubDirs(tmpDir+"htmls\\",subDirList)
print(subDirList)


down.MultiDownImgP(domain,subDirList,"img",True)
#DownImg(subDirList,"small")
#down.MultiDownImgP(domain,subDirList,"small")
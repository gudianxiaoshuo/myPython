from PIL import Image
import matplotlib.pyplot as plt  #数学绘图库
from matplotlib.font_manager import FontProperties #中文字体

from wordcloud import WordCloud,ImageColorGenerator
import numpy as np #科学数值计算包，可用来存储和处理大型矩阵

from head import *

font = FontProperties(fname=fontPath)


#由列表生成词云
def ToWordCloud(list,backImgPath=backImgPath,fontPath=fontPath,maxWords=200):

    listStr="/".join(list)
    #创建有背景的词云图
    image=Image.open(backImgPath)
    graph=np.array(image)

    wc = WordCloud(font_path=fontPath,
                   background_color='white',
                   mask=graph,  # 设置背景图片
                   random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                   # width=1000,
                   # height=700,
                   #max_font_size=100,
                   max_words=maxWords)  # ,min_font_size=10)#,mode='RGBA',colormap='pink')

    wc.generate(listStr)

    # backColor = ImageColorGenerator(graph)  # 从背景图片颜色 生成文字颜色值
    # wc.recolor(color_func=backColor)

    wc.to_file(r"wordcloud.png")

    plt.figure("词云图")
    plt.imshow(wc)
    plt.axis("off")
    plt.show()


#dict权重生成词云
def ToWordCloud_dict(dict_keywords,backImgPath=backImgPath,fontPath=fontPath,maxWords=200):
    '''
    back_coloring = plt.imread(backImgPath)  # 设置背景图片
    # 设置词云属性
    wc = WordCloud(font_path=fontPath,  # 设置字体
                   background_color="white",  # 背景颜色
                   max_words=maxWords,  # 词云显示的最大词数
                   mask=back_coloring,  # 设置背景图片
                   )
    '''
    #创建有背景的词云图
    image=Image.open(backImgPath)
    graph=np.array(image)

    wc = WordCloud(font_path=fontPath,
                   background_color='white',
                   mask=graph,  # 设置背景图片
                   #random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                   # width=1000,
                   # height=700,
                   #max_font_size=200,
                   max_words=maxWords
                   )  # ,min_font_size=10)#,mode='RGBA',colormap='pink')

    # 根据频率生成词云
    wc.generate_from_frequencies(dict_keywords)
    wc.to_file(r"wordcloud.png")
    # 显示图片
    plt.figure()
    plt.imshow(wc)
    plt.axis("off")
    plt.show()

#根据排好序的字典，绘制条状图
def barh_dict(sortedDict,bReverse=False):
    num=len(sortedDict)


    #根据已经排好序的索引列表，创建对应的字符串列表
    newStrList=[x[0] for x in sortedDict]
    #根据已经排好序的索引列表，创建对应的次数列表
    newCountList=[x[1] for x in sortedDict]

    if bReverse:
        newCountList.reverse()
        newStrList.reverse()

    #
    # print("*"*100)
    # print(list(newStrList))
    # print(newCountList)



    plt.barh(range(num),newCountList,color="red",align="center")
    plt.title("中文",
              fontproperties=font,
              fontsize=14
              )


    plt.yticks(range(num),newStrList,
               fontproperties=font,
               fontsize=14
               )
    plt.show()


#初始时，未排序
#根据字符串列表、次数列表，绘制条形图
def barh(strList,countList,bReverse=False):
    '''
    :param strList:     字符串列表
    :param countList:   字符串出现次数
    :return:
    '''
    num=len(strList)
    font = FontProperties(fname="FZSTK.TTF")

    #对次数进行索引排序，排序结果为索引序列，索引对应的值由小到大
    nIndexList=np.argsort(countList)

    #根据已经排好序的索引列表，创建对应的字符串列表
    newStrList=[strList[x] for x in nIndexList]
    #根据已经排好序的索引列表，创建对应的次数列表
    newCountList=[countList[x] for x in nIndexList]

    if(bReverse):
        newStrList.reverse()
        newCountList.reverse()

    plt.barh(range(num),newCountList,color="red",align="center")
    plt.title("中文",
              fontproperties=font,
              fontsize=14
              )

    plt.yticks(range(num),newStrList,
               fontproperties=font,
               fontsize=14
               )
    plt.show()





def test():
    '''
    font= FontProperties(fname="FZSTK.TTF")
    x=range(10)
    plt.plot(x)
    plt.title("中文",
              fontproperties=font,
              fontsize=14
              )
    plt.show()

    :return:
    '''
    strList=["ni","wo","ta"]
    countList=[2,1,6]
    barh(strList,countList)

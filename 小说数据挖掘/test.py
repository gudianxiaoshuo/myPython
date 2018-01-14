
#ecoding=utf-8
import jieba
import jieba.posseg as pseg
#自定义词典
jieba.load_userdict("dict.txt")






#分词

print("*"*100)

seg_list=jieba.cut("欢迎访问我的网站：古典小说网",cut_all=True)
print("Full Mode"+"|".join(seg_list))

seg_list=jieba.cut("欢迎访问我的网站：古典小说网",cut_all=False)
print("精准模式:" +"|".join(seg_list))

seg_list=jieba.cut_for_search("欢迎访问我的网站：古典小说网")
print("搜索引擎模式："+",".join(seg_list))

seg_list=jieba.cut("欢迎访问我的网站：古典小说网")
print("默认精确模式："+",".join(seg_list))



print("*"*100)
#动态给词典加词
jieba.add_word("任性动图")
jieba.add_word("任性小视频")
jieba.add_word("快乐课堂")
jieba.add_word("古典小说大全")
#不是元组，是字符串，元组以逗号隔开
test_sent=("欢迎访问我的网站：古典小说网\n"
           "开发的软件如下:\n"
           "课堂教学类软件：快乐课堂，动图类软件：任性动图，视频编辑类软件：任性小视频，阅读类软件：古典小说大全"
          )
words=jieba.cut(test_sent)
print("|".join(words))
print("="*40)
result=pseg.cut(test_sent)
for w in result:
    print(w.word," ",w.flag,"|",end="  ")


print("\n","="*40)

#提取关键字
#必须导入这个包
import jieba.analyse
str="任性动图软件--你可能没有想过，使用任性动图软件，做动图动画，竟是如此简单"
tag=jieba.analyse.extract_tags(str,5)
print(tag)
print("\n","="*40)
#返回词语位置

str="任性动图软件--你可能没有想过，使用任性动图软件，做动图动画，竟是如此简单"
wPos=jieba.tokenize(str)
for item in wPos:
    print(item)

print("*"*100)
wPos=jieba.tokenize(str,mode="search")
for item in wPos:
    print(item)

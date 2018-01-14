

#第一句要顶格写，而且下面相同层次的还要对齐
import keyword

print(keyword.kwlist)

'''
python语句后面不需要分号，这和 谷歌主推的kotlin 语言一样，或许，以后的新语言，也会采用这种形式。

使用过C的都知道，变量要先声明定义，才能使用，变量有很多类型，本以为php语言用 var就把所有类型包括进去，够省略了，没想到python变量直接不用声明。

python变量直接赋值即可使用，个人理解为这样的状况： 赋值的时候，直接创建赋值内容对应的类型对象，这个解释器可自动判断何种对象，分配好了内存空间，创建好了对象，然后将变量作为标识，分配给这个对象，以便标识使用。

这样一来，解释器自己可根据具体赋值判断何种类型，所以变量就不需要在声明了，直接赋值使用就可以了。​
'''


count=100
miles=1000.0
name="gudianxiaoshuo.com"

print(count)
print(miles)
print(name)

print(isinstance(name,str))

print(name.__len__())
print(type(count))
print(type(miles))
print(type(name))

print("类型转换")
print(int(miles))


#isinstance  \  type

print("test...isinstance  type...")

isinstance(count,int)
isinstance(count,str)
isinstance(count,float)
isinstance(count,(str,int,list))

type(count)
type(name)
type(miles)

#继承类
class A:
    pass

class B(A):
    pass


print(isinstance(A(),A))  #true
print(type(A())==A)       #true
print(isinstance(B(),A))  #true
print(type(B())==A)       #false

# isinstance(object, classinfo)
# 所有的基本类型的classinfo
isinstance(count,(int,float,bool,complex,str,list,dict,set,tuple))





#多个变量赋值
a=b=c=1
print(a)



#print格式化输出 与C语言类似，但实际值用%(,,)表达
print("%s= %d,b=%d" %("a",a,b))


#为多个对象指定多个变量
a,b,c=1,2,"gudianxiaoshuo"

print(c.__len__())


'''
标准数据类型
Number  int float bool complex
String
List
Tuple
Sets
Dictionary

'''

#1、标准数据类型

print("number...")

a,b,c,d=20,5.5,True,4+8j

print("标准数据类型")
print("a=%d,b=%.1f,c=%d,d=%s" %(a,b,c,d))
print(type(a),type(b),type(c),type(d))
bInt=isinstance(a,int)
bFloat=isinstance(b,int)
bBool=isinstance(c,bool)
bComplex=isinstance(d,complex)

print(bInt,bFloat,bBool,bComplex)

#删除对象，释放空间
del a,b,c,d


print("print的使用")
print("我的网站 %s" %("gudianxiaoshuo.com"))

print("小明 %d 岁" %(5))
print("小明身高%.2f米"%(1.65))

print("----------------")
print(2/3)   #0.6666666666666666
print(2//3)  #0  得到整数
print(2%3)   #2  余数
print(2*3)   #6
print(2**3)  #8 乘方
print("----------------")









#2、字符串
#字符串不能改变
# str[nStart,nEnd]  表示的 字符串范围[nStart,nEnd)

print("----------str--------")

str="gudianxiaoshuo.com"
print(str)          # 输出字符串 gudianxiaoshuo.com
print(str[0:-1])    # 输出第0个到倒数第1个之间的所有字符,不包含最后一个 [nStart,nEnd)
                    # gudianxiaoshuo.co

print(str[0])       # 输出字符串第0个字符 g
print(str[2:5])     # 输出从第2个开始到第5个的字符 共3个字符，不包含第5个 dia
print(str[1:])      # 输出从第1个开始的后的所有字符 udianxiaoshuo.com
print(str*2)        # 输出字符串两次  gudianxiaoshuo.comgudianxiaoshuo.com
print(str+" test")  # 连接字符串      gudianxiaoshuo.com test



# \
print("hello \nhello")
print(r"hello \nhello")  #不转义，表示原始字符串

#字符串索引有两种
#从左往右 从0开始
#从右往左 从-1开始

word="gudianxiaoshuo.com"
print(word[0],word[5])   # g n
print(word[-1],word[-3]) # m c

#   word[0]="a"  #字符串不能被改变
#   TypeError: 'str' object does not support item assignment

#3、List列表   []
# 类似于c++的数组，其实是扩展功能的数组

print("----------list--------")

list=['abcd',78,2.2,'hello',1.1]
tinylist=[124,"古典古韵古典小说"]


print(list)          # 输出完整列表 ['abcd', 78, 2.2, 'hello', 1.1]
print(tinylist)      # [124, '古典古韵古典小说']
print(list[0])       # 输出列表第0个元素           abcd
print(list[1:3])     # 从第1个开始输出到第2个元素
print(list[2:])      # 输出从第2个元素开始的所有元素
print(tinylist*2)    # 输出两次列表
print(list+tinylist) # 连接列表
print(list.__len__())# 5

for item in list:    #for循环写法 与C语言不同
    print(item)

print("----------list--------")

a=[1,2,3,4,5,6]
a[0]=9
a[2:5]=[13,14,15]
print(a)
a[2:5]=[]            # 将对应的元素值设置为 []  其实就是删除[2,5)三个元素
print(a)
print(a.__len__())






#4、Tuple元组 ()
#与列表类似，不同之处在于元组不能修改，类似于C++的常量数组

tuple=("aaa",222,2.2,"dd",True,False)
print(tuple)
print(tuple[1:5])
#  tuple[0]=11   非法  不能修改


#空元组
tup1=()

#一个元素 ,需要在元素后添加逗号
tup2=(2,)

print(tup1,tup2)
tup3=tup1+tup2
print(tup3)

'''
string、list和tuple都属于有序的sequence（序列）。
'''

#5  {} 或 set()创建
#
#  集合 无序  不重复
#  创建空集合用set() 而不是 {}
#  {}是创建一个空字典


studentSet={"tom","tom","mary"}
print(studentSet)   #输出集合，重复的元素被自动去掉 {'tom', 'mary'}

#成员测试

if 'Rose' in studentSet:
    print("in set")
else:
    print("not in set")


# set可以进行集合运算
a = set('abracadabra')
b = set('alacazam')


print(a)      #无序的，每次运行，排列顺序都不一样 {'b', 'r', 'd', 'a', 'c'}
print(a - b)  # a和b的差集 {'d', 'b', 'r'}
print(a | b)  # a和b的并集 {'l', 'm', 'b', 'r', 'z', 'd', 'a', 'c'}
print(a & b)  # a和b的交集 {'a', 'c'}
print(a ^ b)  # a和b中不同时存在的元素 {'m', 'b', 'r', 'z', 'd', 'l'}


#字典 Dictionary

print("----------dict--------")

dict={}                    #空字典
dict["one"]="快乐课堂软件"  #
dict[2]="任性动图软件"
dict[3]="任性小视频软件"
dict[4]="古典小说大全"

for key in dict:
    print(key)

for key in dict:
    print(dict[key])

print(dict.keys())
print(dict.values())

print("----------dict--------")
tinydic={"name":"gudianxiaoshuo","code":1,"site":"www.gudianxiaoshuo.com"}

print(dict["one"])
print(dict[2])
print(tinydic)
print(tinydic["code"])
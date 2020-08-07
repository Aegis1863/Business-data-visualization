# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 22:59:54 2020

@author: LeeS
"""

import requests
import bs4
import wordcloud
import jieba
import time
import matplotlib.pyplot as plt

url1='http://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%A\
8%E6%99%AF%E7%82%B9&region=&from=mpl_search_suggest&sort=pp&page='
#爬虫开始
ct=[]
for i in range(14):
    try:
        print('>>>正在爬取第{}页,共14页'.format(i+1))
        time.sleep(0.3)
        r=requests.get(url1+str(i+1))
        r.encoding=r.apparent_encoding
        t=r.text
        soup=bs4.BeautifulSoup(t,'html.parser')
        ct.append(soup)
        print('-->第{}页源码解析完毕'.format(i+1))
    except:
        print('第{}页爬取异常'.format(i+1))
txt=[]
hot=[]
pl=[]
pr=[]
print('>>>正在提取各页文本')
for i in ct:
    b=i.find_all('a',attrs={'class':'name'})
    for p in b:
        txt.append(p.text)
    v=i.find_all('span',attrs={'class':'hot_num'})
    for p2 in v:
        hot.append(p2.text)
    y=i.find_all('span',attrs={'class':'area'})
    for p3 in y:
        pl.append(p3.text.replace('[','').replace(']','').split('·')[0])
    m=i.find_all('span',attrs={'class':'sight_item_price'})
    for p4 in m:
        pr.append(eval(p4.text.replace('¥','').replace('\xa0起','')))
print('>>>提取完毕，开始储存')
with open('data.txt','w') as f:
    f.write(str(txt))
with open('hot.txt','w') as f1:
    f1.write(str(hot))
with open('place.txt','w') as f2:
    f2.write(str(pl))
with open('price.txt','w') as f3:
    f3.write(str(pr))
print('>>>储存完毕,储存位置：程序源码相同目录，储存数据量:\
      2*{},爬虫结束<<<'.format(len(txt)))
#爬虫部分结束

print('\n>>>生成词云中')
po=[]
#手动处理分割词语，有些词语不宜分割或需要合并
for i in ['动物园','海洋公园','欢乐谷','海洋世界','野生动物园']:
    jieba.add_word(i)
for i in ['海洋世界','海洋公园','野生动物园','欢乐谷']:
    jieba.suggest_freq(i)
for i in txt:
    q=jieba.lcut(i)
    for i1 in q:
        if q !='·' and q !='-' and q !='（' and q!='）':
            po.append(i1)
for i in range(len(po)):
    if po[i] == '海洋' or po[i] == '长隆' or po[i] == '水上' or po[i] == '海底' \
    or po[i] == '海洋乐园':
        po[i]='海洋公园'
    elif po[i] == '欢乐':
        po[i]='欢乐谷'
    elif po[i] == '景区':
        po[i]='风景区'
    elif po[i] == '旅游':
        po[i]='旅游区'
    elif po[i] == '乐园' or po[i]=='王国':
        po[i]='欢乐谷'
    elif po[i]=='野生动物园':
        po[i]='动物园'

for i in po[::-1]:
    if i == '世界' or i== '国色' or i== '天乡'or i=='东方' or i=='海昌' or\
    i=='野生动物' or i == '极地':
        po.remove(i)
#处理结束

tx = " ".join(po)
w = wordcloud.WordCloud(font_path ='simhei.ttf',width = 1000, height=700,\
                        background_color="white",max_words =200)
w.generate(tx)
print('>>>词云生成完毕，保存在程序目录，文件名：wordcloud.png')
w.to_file("wordcloud.png")

print('>>>开始统计词频')
counts={}
for word in po:
    if len(word)==1:
        continue
    else:
        counts[word] = counts.get(word,0)+1
items = list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
print('-->景点词频较大排名前{:2}项：'.format(20))
for i in range(20):
    word,count = items[i]
    print('{0:<5}{1:>5}'.format(word,count))
print()

counts1={}

for word in pl:  #排序
    counts1[word] = counts1.get(word,0)+1
items1 = list(counts1.items())
items1.sort(key=lambda x:x[1],reverse=True)
print('-->地区词频较大排名前{:2}项：'.format(20))
for i in range(20):
    word1,count1 = items1[i]
    print('{0:<5}{1:>5}'.format(word1,count1,))
print()
#词频统计结束

#开始可视化视图
print('>>>生成可视化图表')
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
data1=[]#总景点分类
data2=[]#景点类型词频
data3=[]#被删除的景点类型
data4=[]#被删除的景点类型数据
data5=[]#保留的景点类型
data6=[]#保留的景点类型词频
data7=[]#地点分类
data8=[]#地点词频
#对前14个数据进行统计分析
for i in range(14):
    word,count=items[i]
    data1.append(word)
    data2.append(count)
for i in range(20):
    word1,count1=items1[i]
    data7.append(word1)
    data8.append(count1)

#筛出标题中的地点,只展示标题中景区类型
for i in range(14):
    if data1[i]=='上海' or data1[i]=='成都' or data1[i]=='南昌' or data1[i]=='天津'\
    or data1[i]=='北京' or data1[i]=='青岛' or data1[i]=='南京' or data1[i]=='重庆'\
    or data1[i]=='武隆':
        data3.append(data1[i])
        data4.append(data2[i])
    else:
        data5.append(data1[i])
        data6.append(data2[i])

plt.figure(1)
plt.title('景区排名')
plt.xticks(rotation=45)
plt.bar(data5, data6, ec='g',ls='-',color=['r','coral','orange','lightgreen','c'\
                                           ,'skyblue','slategray','lightsteelblue'])
plt.show()

plt.figure(2)
plt.title('地区排名')
plt.xticks(rotation=45)
plt.pie(data8, 
        labels = data7, autopct = '%3.1f%%',\
        startangle = 180,colors = ['r','coral','orange','lightgreen','c'\
                                           ,'skyblue','slategray','lightsteelblue'])
plt.show()

dist={}
hot1=[]
lo=[]
pri=[]
for i in range(len(txt)):
    dist[txt[i]]=pr[i]
for key in dist:
    if '欢乐谷' in key or '欢乐世界' in key or '方特' in key:
        lo.append(key)
        pri.append(dist[key])
plt.figure(3) #创建图像
plt.xticks(rotation=45) #x坐标文字倾斜45度
plt.bar(lo, pri, ec='g',ls='-',color=['r','coral','orange','lightgreen','c'\
                                           ,'skyblue','slategray','lightsteelblue'])
plt.title('欢乐谷类型景点票价')
plt.show()

plt.figure(4)
for i in range(len(txt)):
    for g in lo:
        if g==txt[i]:
            hot1.append(int(hot[i]))
plt.xticks(rotation=45)
plt.bar(lo, hot1, ec='g',ls='-',color=['r','coral','orange','lightgreen','c'\
                                           ,'skyblue','slategray','lightsteelblue'])
plt.title('欢乐谷类型景点月销量')
plt.show()

plt.figure(5)
sale = []
for i in range(len(hot1)):
    sale.append(hot1[i]*pri[i])
plt.xticks(rotation=30)
plt.bar(lo,sale,color=['r','coral','orange','lightgreen','c'\
                                           ,'skyblue','slategray','lightsteelblue'])
plt.title('月销售额')
plt.show()

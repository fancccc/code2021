# -*- coding: utf-8 -*-
"""
Created on Mon May 10 23:27:01 2021

@author: Mario
"""

import pandas as pd
from snownlp import SnowNLP
from snownlp import sentiment
import random
import jieba
import imageio
from wordcloud import WordCloud,ImageColorGenerator
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import TreeMap
from matplotlib.patches import ConnectionPatch

plt.rcParams['font.sans-serif']=['SimHei']
#sentiment.train('neg.txt', 'pos.txt')
#sentiment.save('QuanShi.marshal')

df = pd.read_csv('AllData.csv',encoding = 'gb18030')
df['ZAN'] = df['ZAN'].replace('list index out of range',0)
df['ZAN'] = df['ZAN'].apply(int)
'''
lis = df['comment'][80:100].tolist()
for text in lis:
    s = SnowNLP(text)
    print(text,'\n',s.sentiments)

#df.dropna(subset=['comment'],inplace=True)
qs = []
for i in df['comment'].tolist():
    try:
        qs.append(SnowNLP(i).sentiments)
    except:
        qs.append(0)
df['拳师score'] = qs
df['拳师'] = df['拳师score'].apply(lambda x:'yes' if x >= 0.5 else 'no')
df.to_csv('AllData.csv',index = 0,encoding = 'gb18030')
'''
dfY = df[df['拳师'] == 'yes']
dfN = df[df['拳师'] == 'no']
for example in random.sample(dfY['comment'].tolist(), 10):
    print(example)
sex_propor = len(dfY[dfY['sex'] == '女']) / len(dfY)
print(sex_propor)

# 绘制词云
def draw_wordcloud(s,filename):
    #读入一个txt文件
    comment_text = s
    #结巴分词，生成字符串，如果不通过分词，无法直接生成正确的中文词云
    cut_text = " ".join(jieba.cut(comment_text))
    #color_mask = imageio.imread("rock.png") # 读取背景图片
    #color_mask = np.array(Image.open('rock.png'))
    cloud = WordCloud(
        font_path = 'msyhl.ttc',
        #设置背景色
        background_color = 'white',
        #词云形状
        #mask = color_mask,
        #允许最大词汇
        max_words = 2000,
        #最大号字体
        max_font_size = 50,
        scale = 6,#分辨率
    )
    word_cloud = cloud.generate(cut_text) # 产生词云
    plt.figure(figsize = (10,10),dpi = 80)
    word_cloud.to_file('img/'+filename) #保存图片
    plt.axis('off')
    #  显示词云图片
    plt.imshow(word_cloud)

s = ''
for i in dfN['comment']:
    s += str(i) + '。'
draw_wordcloud(s,'非女权.png')

s = ''
for i in dfY['comment']:
    s += str(i) + '。'
draw_wordcloud(s,'女权.png')

plt.figure(dpi = 120)
x = [len(dfY), len(dfN)]
explode = [0.1,0.01]
labels = ['拳师','非拳师']
plt.pie(x = x,
        explode = explode,
        labels = labels,
        autopct = '%3.2f%%')
plt.title('总体分布')
plt.savefig('img/总体分布.png')
plt.show()

plt.figure(dpi = 120)
x = [len(dfY[dfY['sex'] == '女']), len(dfY[dfY['sex'] == '男'])]
explode = [0.01,0.01]
labels = ['女','男']
plt.pie(x = x,
        explode = explode,
        labels = labels,
        autopct = '%3.2f%%')
plt.title('性别')
plt.savefig('img/性别.png')
plt.show()

plt.figure(figsize=(15,15),dpi = 120)
df_acre = df.groupby('acre')['id'].count()
x = df_acre.values
labels = df_acre.index
explode = [0.001] * len(x)
plt.pie(x = x,
        explode = explode,
        labels = labels,
        autopct = '%3.2f%%')
plt.title('地区')
plt.savefig('img/地区.png')
plt.show()

df['lable'] = df['拳师score'].apply(lambda x:1 if x >= 0.5 else 0)
replyY = dfY['reply'].mean()
replyN = dfN['reply'].mean()
weiboY = dfY['weibo'].mean()
weiboN = dfN['weibo'].mean()
befanY = dfY['befan'].mean()
befanN = dfN['befan'].mean()
fanY = dfY['fan'].mean()
fanN = dfN['fan'].mean()
zanY = dfY['ZAN'].mean()
zanN = dfN['ZAN'].mean()
plt.figure(dpi = 120)
x = ['回复数(评论)','点赞数(评论)','微博数','关注数','粉丝数']
index = np.arange(len(x))
bar_width = 0.45
y1 = [replyY, zanY, weiboY, befanY, fanY]
y2 = [replyN, zanN, weiboN, befanN, fanN]
plt.bar(index, y1, bar_width, label = '女权')
plt.bar(index+bar_width, y2, bar_width, label = '非女权')
plt.xticks(index+bar_width/2, x)
plt.legend()
plt.title('数据对比')
plt.xlabel('指标均值')
for a,b in zip(index,y1):
    plt.text(a, b+10,'%.1f'%b, ha = 'center',va = 'bottom')
for a,b in zip(index,y2):
    plt.text(a+bar_width, b+10,'%.1f'%b, ha = 'center',va = 'bottom')
plt.savefig('img/各项指标分析.png')
plt.show()

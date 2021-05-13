# -*- coding: utf-8 -*-
"""
Created on Sun May  9 21:40:28 2021

@author: Mario
"""

from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
import json
import pandas as pd
from selenium.webdriver import ActionChains
from snownlp import SnowNLP
from snownlp import sentiment
#全局变量

def get_info(html):    
    soup = BeautifulSoup(html,'lxml')
    lis = soup.find_all('div',attrs={'class':'c'})
    data = []
    for j in range(2,len(lis)):
        info = []
        try:
            info.append(lis[j].a['href'])#主页
            info.append(lis[j].a.text)#id
            info.append(lis[j].span.text)#评论
            info.append(re.findall('\d+',lis[j].text.split('\xa0')[-4])[0])#赞
            info.append(lis[j].text.split('\xa0')[-2])#time
            info.append(lis[j].text.split('\xa0')[-1])#来源
        except Exception as e:
            print(j)
            info.append(e)  
        data.append(info)
    return data
def get_web_info(n, html):#网页端
    soup = BeautifulSoup(html,'lxml')
    lis = soup.find_all('div',attrs={'class':'list_li S_line1 clearfix'})
    info = []
    for i in range(n,len(lis)):
        data = []
        try:
            data.append(lis[i].div.a['href'])#link
            data.append(lis[i].div.img['alt'])#id
            data.append(lis[i].find(class_ = 'WB_text').text.split('：')[1].strip())#评论
            data.append(lis[i].find(class_ = 'WB_from S_txt2').text)#time
            data.append(re.findall('\d+',lis[i].find(class_ = 'WB_handle W_fr').text)[0])#点赞数
            try:
                data.append(re.findall('共\d+',lis[i].find(class_ = 'list_li_v2').text)[0].strip('共'))#回复数
            except:
                data.append(0)
        except Exception as e:
            data.append(e)
        finally:
            info.append(data)
    return info
    
'''    
driver = webdriver.Chrome('E:\Files\Google\Chrome\Application\chromedriver.exe')
driver.get('https://weibo.cn/comment/hot/KecJ9pKQ6?rl=1&page=1')
#https://weibo.com/2794430491/KecJ9pKQ6?filter=hot&root_comment_id=0&type=comment
x = input('login:')
data = []
nu = 0
while True:
    print('********爬取%d条********' % nu)
    html = driver.page_source
    d = get_web_info(nu, html)
    nu += len(d)
    for x in d:
        with open('com.txt','a', encoding = 'gb18030')as f:
            for s in x:
                f.write(str(s) + '\t')
            f.write('\n')
    #data += d
    try:
        ActionChains(driver).move_by_offset(0, 0).click().perform()
        driver.find_element_by_xpath("//div[@class='list_ul']/a/span").click()
    except Exception as e:
        print(e)
        break
'''   
#df = pd.DataFrame(data)
#df.columns = ['link', 'id', 'comment', 'date', 'ZAN', 'reply']

'''
if x == 'y':
    data = []
    for i in range(600):
        ActionChains(driver).move_by_offset(0, 0).click().perform()
        print('#####第{}页#####'.format(i+1))
        time.sleep(0.5)
        html = driver.page_source
        data += get_info(html)
        driver.find_element_by_xpath("//div[@class='pa']/form/div/a").click()
df = pd.DataFrame(data)    
df.columns = ['link','id','comment','zan','time','from']
df = df.drop_duplicates(keep='first',subset=['id','comment'])

data_info = []
for i in df['link']:
    driver.get('https://weibo.cn/' + i.split('/')[-1])
    #微博数、粉丝数、关注数
    strCnt = driver.find_element_by_xpath("//div[@class='tip2']")
    pattern = r"\d+\.?\d*"      # 匹配数字，包含整数和小数
    cntArr = re.findall(pattern, strCnt.text)
    #性别
    strInf = driver.find_element_by_xpath("//div[@class='ut']")
    sex = re.findall('[男女]',strInf.text)[0]
    arce = strInf.text.split('/')[1].split()[0]
    sign = strInf.text.split('/')[1].split()[2]
    #link sex 地区 签名 微博数 关注数 粉丝数
    data_info.append([i, sex, arce, sign, cntArr[0], cntArr[1], cntArr[2]])
data_info = [i[0] for i in data_info]
df_info = pd.DataFrame(data_info)
df_info.columns = ['link','sex','地区','签名','微博数','关注数', '粉丝数']

df_info = df_info.drop_duplicates(keep='first')
df = pd.merge(df,df_info,how = 'left')
df.to_csv('info.csv',index = 0,encoding = 'gb18030')
'''
#sentiment.train('neg.txt', 'pos.txt')
#sentiment.save('QuanShi.marshal')
lis = df['comment'][100:110].tolist()
#text = '你已经很棒了 '
for text in lis:
    s = SnowNLP(text)
    print(text,'\n',s.sentiments)
df.dropna(subset=['comment'],inplace=True)
qs = []
for i in df['comment'].tolist():
    try:
        qs.append(SnowNLP(i).sentiments)
    except:
        qs.append(0)
df['拳师score'] = qs
df['拳师'] = df['拳师score'].apply(lambda x:'yes' if x >= 0.5 else 'no')
df.to_csv('infoNew.csv',index = 0,encoding = 'gb18030')
#!/usr/bin/env python
# coding: utf-8

import requests
import re
import pandas as pd

headers ={ 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}
URL = 'http://www.xyszj.gov.cn/index.php?m=content&c=index&a=lists&catid=49&page='
data_list = []
name_list = []

def getname(url):
    response = requests.get(url,headers=headers)
    pat_0 = '<span class="time">(.*?)</span>'
    pat_1 = 'target="_blank" style="" >(.*?)</a></li>'
    pat_2 = '<a href=(.*?) target="_blank" style="" >'
    rst_0 = re.compile(pat_0).findall(response.text)
    rst_1 = re.compile(pat_1).findall(response.text)
    rst_2 = re.compile(pat_2).findall(response.text)

    for y in range(0, len(rst_0)):
        name_list.append({
            '预售时间': rst_0[y],
            '项目名称': rst_1[y],
            '链接': rst_2[y]
        })

def getnumber(url1):
    response = requests.get(url1, headers=headers)
    pat = '<td height="40" align="left" valign="top">(.*?)</td>'
    pat0 = '<div class="xken">(.*?)</div>'
    pat1 = '<td height="54" align="left" valign="top">(.*?)</td>'
    pat2 = 'valign="middle">(.*?)</td>'
    pat3 = ' <div class="ngs8">(.*?)</div>'
    pat4 = ' <div class="ngs9">(.*?)</div>'
    pat5 = ' <div class="ngs10">(.*?)</div>'

    rst = re.compile(pat).findall(response.text)
    rst0 = re.compile(pat0).findall(response.text)
    rst1 = re.compile(pat1).findall(response.text)
    rst2 = re.compile(pat2).findall(response.text)
    rst3 = re.compile(pat3).findall(response.text)
    rst4 = re.compile(pat4).findall(response.text)
    rst5 = re.compile(pat5).findall(response.text)
    for y in range(0, len(rst2) - 1, 6):
        data_list.append({
            '售房单位': rst[0],
            '项目名称': rst[1],
            '预售证号': rst0[0],
            '批售时间': rst3[0] + '/' + rst4[0] + '/' + rst5[0],
            '房屋坐落': rst1[0],
            '楼号': rst2[y],
            '结构': rst2[y + 1],
            '层数': rst2[y + 2],
            '房屋用途': rst2[y + 3],
            '建筑面积': rst2[y + 4],
            '住宅套数': rst2[y + 5]
        })

page = 1
bage = '2'
while page < int(bage) + 1:
    url = URL + str(page)
    getname(url)
    page = page +1

name_list = pd.DataFrame(name_list)
lis = list(name_list['链接'])
i = 0
while i < len(lis):
    getnumber(eval(lis[i]))
    i = i+1

data_list = pd.DataFrame(data_list)
#data_list.to_excel('项目明细数据.xlsx', encoding="gbk", index=False)
#df = pd.read_excel('项目明细数据.xlsx')

df1 = data_list.dropna(subset = ['楼号','结构','层数','房屋用途'])
df1['房屋用途'] = df1['房屋用途'].str.replace('    ', '<br/>')
df1['房屋用途'] = df1['房屋用途'].str.replace(' ', '')
df1['建筑面积'] = df1['建筑面积'].str.replace(' ', '')

df0 = df1.loc[~df1['房屋用途'].isin(['住宅<br/>非住宅'])]

df2 = df1.loc[df1['房屋用途'].isin(['住宅<br/>非住宅'])]
df2['房屋用途'] = df2['房屋用途'].str.split("<br/>").str[-1]
df2['建筑面积'] = df2['建筑面积'].str.split("<br/>").str[-1]
df2['住宅套数'] = 0

df3 = df1.loc[df1['房屋用途'].isin(['住宅<br/>非住宅'])]
df3['房屋用途'] = df3['房屋用途'].str.split("<br/>").str[0]
df3['建筑面积'] = df3['建筑面积'].str.split("<br/>").str[0]

df4 = pd.concat([df0,df2,df3],axis=0,ignore_index=True)
df4['建筑面积'] = df4['建筑面积'].str.split("：").str[-1]
df4.loc[df4.房屋用途=='非住宅','住宅套数'] = 0
df4['层数'] = df4['层数'].str.replace('   ', '<br/>')
df4['层数'] = df4['层数'].str.replace(' ', '')
df4['层数'] = df4['层数'].str.replace('<br/>', '、')
df4['层数'] = df4['层数'].str.replace('</br>', '、')
df4.to_excel('咸阳预售数据.xlsx', encoding="gbk", index=False)

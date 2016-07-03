from multiprocessing import Pool
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pandas as pd


def get_info(id):
    url='http://192.168.1.235:7001/default/com.dszxx.portal.xxb.LetterDetial.flow?id={}'.format(id)
    wb_data=requests.get(url)
    soup=BeautifulSoup(wb_data.text,'lxml')
    if soup.select('ul.genzong li')==[]:
        print('页码{}无内容'.format(id))
    else:
        title=soup.select('body > div.container > div.content > div.rightside > div > div.mailtop > p.marbottom10.martop10.txtindent28.font16.colorfff.txtbold')[0].get_text().strip()
        content=soup.select('body > div.container > div.content > div.rightside > div > div.mailneirong > p.marbottom10.martop10.txtindent28')[0].get_text().strip()
        replyer=list(soup.select('ul.genzong li')[-1].stripped_strings)[0].strip().split(' ')[1].strip().split('  ')[-1]
        replydate=list(soup.select('ul.genzong li')[-1].stripped_strings)[0].strip().split(' ')[0]
        date=soup.select('body > div.container > div.content > div.rightside > div > div.mailtop > p.relative > span')[0].get_text().strip().split(' ')[0]
        driver.get(url)
        driver.implicitly_wait(30)
        try:
            replycontent = driver.find_element_by_xpath('//*[@id="con"]/div[1]/p[2]').text

        except:
            replycontent=""
            print("无回复内容")
        data={
        '标题':[title,0],
        '来信日期':[date,0],
        '回复单位':[None if replyer=='' else replyer.split('\xa0')[-1],0],
        '回复日期':[replydate,0],
        '来信内容':[content,0],
        '回复内容':[replycontent,0],
        'link':[url,0],
        'id':[id,0]
         }
        return data
#统计已获取列表
data1={
            '标题':['标题','标题'],
            '来信日期':['标题','标题'],
            '回复单位':['标题','标题'],
            '回复日期':['标题','标题'],
            '来信内容':['标题','标题'],
            '回复内容':['标题','标题'],
            'link':['标题','标题'],
            'id':['标题','标题']
        }
df_get=pd.DataFrame(data1,columns=['标题','来信日期','回复单位','回复日期','来信内容','回复内容','link','id'])
df_get=df_get.drop(1)
df_get=df_get.drop(0)

path='C:/Users/Administrator/Desktop/董事长信箱解答/董事长信箱记录导出'
df_previous=pd.read_csv(path+"/董事长信箱.csv", encoding='gbk')
driver = webdriver.PhantomJS(executable_path=path+"/phantomjs-2.1.1-windows/bin/phantomjs.exe")
#num1=input('请输入最新的信箱编码：')
#num2=input('请输入要查找信件数量：')
df=df_previous['id']
for i in df.index:
    id=df[i]
    print(i,id)
    data=get_info(int(id))
    if data:
        frame=pd.DataFrame(data,columns=['标题','来信日期','回复单位','回复日期','来信内容','回复内容','link','id'])
        frame=frame.drop(1)
        df_get=df_get.append(frame)

driver.quit()
#df_main=df_get.append(df_previous)
#df_main.drop_duplicates()
df_get.to_csv(path+"/董事长信箱1.csv",indes=False)




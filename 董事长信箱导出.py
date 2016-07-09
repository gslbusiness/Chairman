from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
import pandas as pd

#统计已获取列表

#df_get=pd.DataFrame(columns=['标题','来信日期','回复单位','回复日期','来信内容','回复内容','link','id'])
df_get=pd.read_csv(path+"/董事长信箱1.csv", encoding='gbk')
path='C:/Users/Administrator/Desktop/董事长信箱解答/董事长信箱记录导出'
df_previous=pd.read_csv(path+"/董事长信箱.csv", encoding='gbk')
df_id=df_previous[~df_previous['id'].isin(df_get['id'])]
driver = webdriver.PhantomJS(executable_path=path+"/phantomjs-2.1.1-windows/bin/phantomjs.exe")

df=df_id['id']
for i in df.index:
    id=df[i]
    print(i,id)
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
        df_get.loc[len(df_get)+1]=[title,date,None if replyer=='' else replyer.split('\xa0')[-1],replydate,content,replycontent,url,id]
driver.quit()
df_get.to_csv(path+"/董事长信箱1.csv",index=False)

from selenium import webdriver
import bs4
from selenium import webdriver
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import selenium
from selenium.webdriver.common.keys import Keys
import requests

# chromedriver로 웹사이트 열기

driver= webdriver.Chrome("/Users/taehopark/PycharmProjects/dalchaebi/Scrapping/HIDOC/chromedriver")
driver.get("https://www.hidoc.co.kr/healthqna/list")
# scrap 할 내용을 page source로 저장 (html) 정보를 리스트로 저장
html = driver.page_source
bs= bs4.BeautifulSoup(html,"html.parser")
total_number= bs.find("dd",attrs={"id":"countQna"}).text
total_number = int(total_number.replace(",",""))
page_num= (total_number//7)+1

# 빈 리스트 생성

lst_questions=[]
lst_name_docs=[]
lst_name_hospitals =[]
lst_descriptions=[]
lst_pg_num=[]

URL = "https://www.hidoc.co.kr/healthqna/list?page="

for i in range(1,page_num+1):
    URL_page = URL+str(i)
    url_requests = requests.get(URL_page)
    url_soup = BeautifulSoup(url_requests.text,'html.parser')
    questions = bs.find_all("strong", attrs={"class":"tit_qna"})
    name_docs=bs.find_all("a", attrs={"class":"link_doctor"})
    name_hospitals =bs.find_all("span", attrs={"class":"txt_clinic"})
    descriptions = bs.find_all("p", attrs={"class":"desc"})

    for j in range(len(questions)):
        lst_questions.append(questions[j])
        lst_name_docs.append(name_docs[j])
        lst_name_hospitals.append(name_hospitals[j])
        lst_descriptions.append(descriptions[j+1])
    print(i)
df = pd.DataFrame(zip(lst_questions,lst_name_docs,lst_name_hospitals,lst_descriptions))
df.rename(columns={0:'질문',1:'의사명',2:'병원명',3:'설'},inplace=True)
df.to_excel("hidoc.xlsx",index=False)
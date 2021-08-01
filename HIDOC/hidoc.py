from selenium import webdriver
import bs4
from selenium import webdriver
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import selenium
from selenium.webdriver.common.keys import Keys
import requests
import time


# 창 숨기는 옵션 추가
options = webdriver.ChromeOptions()
options.add_argument("headless")

# chromedriver로 웹사이트 열기
driver= webdriver.Chrome("/Users/taehopark/PycharmProjects/dalchaebi/Scrapping/HIDOC/chromedriver",options=options)
driver.get("https://www.hidoc.co.kr/healthqna/part/list?code=PY000&page=1")
# scrap 할 내용을 page source로 저장 (html) 정보를 리스트로 저장
html = driver.page_source
bs= bs4.BeautifulSoup(html,"html.parser")
total_number= bs.select('div[class="tit_summary"]>strong')[0].text.replace("산부인과","")
total_number = int(total_number.replace(",",""))
page_num= (total_number//7)+1
print(page_num)

# 빈 리스트 생성

lst_titles=[]
lst_questions=[]
lst_question_time=[]
lst_name_docs=[]
lst_answers=[]

URL = "https://www.hidoc.co.kr/healthqna/part/list?code=PY000&page="

for i in range(1001,2001):
    #Selenium용 Parsing
    URL_page = URL+str(page_num-i)
    driver.get(URL_page)
    html = driver.page_source
    bs = bs4.BeautifulSoup(html, "html.parser")
    elems = driver.find_elements_by_class_name("desc")

    for x in range(0,len(elems)):
        elems=driver.find_elements_by_class_name("desc")
        elems[x].click()
        url_requests = driver.page_source
        url_soup = BeautifulSoup(url_requests,'html.parser')
        titles=url_soup.select_one("strong.tit").text
        question_time = url_soup.select_one("span.txt_time").text
        questions = url_soup.select('div[class="box_type1 view_question"]>div[class="inner"]>div[class="desc"]>p')[0].get_text()
        num_answer = len(url_soup.select('div[class="box_type1 hidoc_answer"]>div[class="answer_body"]>div[class="cont"]>div[class="desc"]'))

        if titles in lst_titles:
            if num_answer !=2:
                answers = url_soup.select('div[class="box_type1 hidoc_answer"]>div[class="answer_body"]>div[class="cont"]>div[class="desc"]')[2].get_text()
            else:
                answers = url_soup.select(
                    'div[class="box_type1 hidoc_answer"]>div[class="answer_body"]>div[class="cont"]>div[class="desc"]')[
                    0].get_text()
        elif titles not in lst_titles:
            answers = url_soup.select('div[class="box_type1 hidoc_answer"]>div[class="answer_body"]>div[class="cont"]>div[class="desc"]')[0].get_text()
        lst_titles.append(titles)
        lst_question_time.append(question_time)
        lst_questions.append(questions)
        lst_answers.append(answers)
        driver.back()
    print(page_num-i)
df = pd.DataFrame(zip(lst_titles,lst_question_time,lst_questions,lst_answers))
df.rename(columns={0:'제목',1:'질문 시간',2:'질문',3:'답변'},inplace=True)
df.to_excel("hidoc.xlsx",index=False)
index = len(df)
with open("hidoc_questions.txt",'w') as f:
    for j in range(index):
        f.write(df['질문'][j]+'\n')
with open("hidoc_answer.txt",'w') as f:
    for i in range(index):
        f.write(df['답변'][i]+'\n')
print(df)
driver.quit()
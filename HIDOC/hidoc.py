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
driver= webdriver.Chrome("/Users/taehopark/PycharmProjects/dalchaebi/Scrapping/HIDOC/chromedriver")
driver.get("https://www.hidoc.co.kr/healthqna/list")
# scrap 할 내용을 page source로 저장 (html) 정보를 리스트로 저장
html = driver.page_source
bs= bs4.BeautifulSoup(html,"html.parser")
total_number= bs.find("dd",attrs={"id":"countQna"}).text
total_number = int(total_number.replace(",",""))
page_num= (total_number//7)+1

# 빈 리스트 생성

lst_titles=[]
lst_questions=[]
lst_question_time=[]
lst_name_docs=[]
lst_name_hospitals =[]
lst_answers=[]

URL = "https://www.hidoc.co.kr/healthqna/list?page="

for i in range(1,10):
    #Selenium용 Parsing
    URL_page = URL+str(i)
    driver.get(URL_page)
    html = driver.page_source
    bs = bs4.BeautifulSoup(html, "html.parser")
    elems = driver.find_elements_by_class_name("desc")
    print(len(elems))
    for x in range(1,len(elems)):
        elems=driver.find_elements_by_class_name("desc")
        elems[x].click()
        url_requests = driver.page_source
        url_soup = BeautifulSoup(url_requests,'html.parser')
        titles=url_soup.select_one("strong.tit").text
        question_time = url_soup.select_one("span.txt_time").text
        questions = url_soup.select('div[class="box_type1 view_question"]>div[class="inner"]>div[class="desc"]>p')[0].get_text()
        if titles == "당뇨 망막증":
            answers = url_soup.select(
                'div[class="box_type1 hidoc_answer"]>div[class="answer_body"]>div[class="cont"]>div[class="desc"]')[
                0].get_text()
            name_hospitals = url_soup.find("span", attrs={"class": "txt_clinic"})
            if type(name_hospitals) == bs4.element.Tag:
                name_hospitals = name_hospitals.text
            else:
                name_hospitals = '0'
        elif titles in lst_titles:
            answers = url_soup.select('div[class="box_type1 hidoc_answer"]>div[class="answer_body"]>div[class="cont"]>div[class="desc"]')[2].get_text()
            name_hospitals = url_soup.select('span[class= "txt_clinic"]')[1]
            if type(name_hospitals) == bs4.element.Tag:
                name_hospitals = name_hospitals.get_text()
            else:
                name_hospitals = '0'
        elif titles not in lst_titles:
            answers = url_soup.select('div[class="box_type1 hidoc_answer"]>div[class="answer_body"]>div[class="cont"]>div[class="desc"]')[0].get_text()
            name_hospitals = url_soup.find("span", attrs={"class": "txt_clinic"})
            if type(name_hospitals) == bs4.element.Tag:
                name_hospitals = name_hospitals.text
            else:
                name_hospitals = '0'

        lst_titles.append(titles)
        lst_question_time.append(question_time)
        lst_questions.append(questions)
        lst_name_hospitals.append(name_hospitals)
        lst_answers.append(answers)
        driver.back()

    print(i)
df = pd.DataFrame(zip(lst_titles,lst_question_time,lst_questions,lst_name_hospitals,lst_answers))
df.rename(columns={0:'제목',1:'질문 시간',2:'질문',3:'병원 이름', 4:'답변'},inplace=True)
df.to_excel("hidoc.xlsx",index=False)
print(df)
driver.quit()
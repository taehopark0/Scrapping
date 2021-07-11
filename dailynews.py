from selenium import webdriver
import bs4
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("/Scrapping/chromedriver")
driver.get("https://google.co.kr/")
elem = driver.find_element_by_name("q") # 검색창 지정
elem.send_keys(" ") #넣고 싶은 키워드
elem.send_keys(Keys.RETURN) # 엔터
time.sleep(0.3)

tabs = driver.find_elements_by_class_name("hdtb-mitem")
news_tab = tabs[2]
news_tab.click()

tools = driver.find_element_by_class_name("t2vtad")
tools.click()
time.sleep(0.3)

# 일자 설정 팝업 탭 찾기
popup_tab = driver.find_elements_by_class_name("KTBKoe")
duration = popup_tab[1]
duration.click()
time.sleep(0.5)

# 지난 1일로 일자 설정 클릭
time_tab =driver.find_element_by_xpath('//*[@id="lb"]/div/g-menu/g-menu-item[3]/div/a').click()

#페이지 반복
html = driver.page_source
bs= bs4.BeautifulSoup(html,"html.parser")

page_num = bs.find_all("a",attrs={"class":"fl"})
pg_num_list = []
for pg_num in page_num:
    pg_num_list.append(pg_num.text)

page_number = 1
headline_list=[]
url_list=[]
while str(page_number) in pg_num_list or str(page_number+1) in pg_num_list:
    html = driver.page_source
    bs = bs4.BeautifulSoup(html, "html.parser")
    page_num = bs.find_all("a", attrs={"class": "fl"})
    pg_num_list = []
    for pg_num in page_num:
        pg_num_list.append(pg_num.text)
    # 스크롤 다운
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# 뉴스 헤드라인 및 url 찾기

    urls = bs.find_all("a", attrs={"style":"text-decoration:none;display:block"})
    headlines = bs.find_all("div", attrs={"class":"JheGif nDgy9d"})

    for i in range(len(urls)):
        headline_list.append(headlines[i].text)
        url_list.append(urls[i].attrs["href"])
    elem = driver.find_elements_by_class_name("fl")
    if str(page_number+1) not in pg_num_list: #마지막 페이지에서 클릭을 못하게 하기 위함
        break
    elem[page_number].click()
    page_number+=1

df = pd.DataFrame(zip(headline_list,url_list))
df.rename(columns={0:'Title',1:'URL'},inplace=True)
df.to_excel('daily_news.xlsx',index=False)
print(df)
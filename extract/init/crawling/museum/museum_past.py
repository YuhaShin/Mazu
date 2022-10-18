from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re

driver = webdriver.Chrome(executable_path='C:\workspaces\workspace_crawling\drivers\chromedriver.exe')

target_url ='https://www.museum.go.kr/site/main/exhiSpecialTheme/list/past?cp=1&pageSize=9&sortOrder=EXHI_SP_THEM_START&sortDirection=DESC&unitedUse=ecms&selectTime=past&currentTime=2022-08-29'
driver.get(target_url)
sleep(3)

#마지막 페이지를 알기위해 우선 접속
soup = BeautifulSoup(driver.page_source, 'html.parser')
last_page_link = soup.select_one('div[class=m-pagenation] > a:last-child')['href']
last_page_num = int(last_page_link[last_page_link.find('cp')+3:last_page_link.find('pageSize')-1])

col_list = ['exhibition_name', 'poster_link', 'exhibition_description', 'exhibition_period', 'exhibition_place']
row_list = []
for page_num in range(1, last_page_num+1):
    target_url = f'https://www.museum.go.kr/site/main/exhiSpecialTheme/list/past?cp={page_num}&pageSize=9&sortOrder=EXHI_SP_THEM_START&sortDirection=DESC&unitedUse=ecms&selectTime=past&currentTime=2022-08-29'
    driver.get(target_url)
    sleep(3)

    #페이지별 전시회 갯수 탐색
    exhibition_list = driver.find_elements(By.CSS_SELECTOR,'.show-list.report.special > li')

    for idx, driver_li in enumerate(exhibition_list):
        value_list = []
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        exhibition_box = soup.select('.show-list.report.special > li')[idx]
        poster_link = 'https://www.museum.go.kr/' + exhibition_box.select_one('div[class=exhioversea-img-over]').find_next_sibling()['src']
        exhibition_name = exhibition_box.select_one('div[class=info] strong').text
        exhibition_period = exhibition_box.select('div[class=info] p')[0].text
        exhibition_place = exhibition_box.select('div[class=info] p')[1].text
        driver_li.find_element(By.TAG_NAME,'a').send_keys(Keys.ENTER)
        sleep(3)

        #데이터 추출(description)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        exhibition_description = soup.select_one('div[class=view-info-cont]').text
        #description_html = soup.select_one('div[class=view-info-cont]')
        #exhibition_description = ' '.join(re.compile('[가-힣]+').findall(str(description_html)))

        value_list.append(exhibition_name)
        value_list.append(poster_link)
        value_list.append(exhibition_description)
        value_list.append(exhibition_period)
        value_list.append(exhibition_place)
        #value_list.append(description_html)
        row_list.append(value_list)

        #뒤로가기
        driver.back()
        sleep(3)


middle_museum_df = pd.DataFrame(row_list, columns=col_list)

middle_museum_df.to_csv('국립중앙박물관_past.csv', encoding="utf-8-sig")
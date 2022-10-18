from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from time import sleep
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re
from datetime import datetime

#driver = webdriver.Chrome(executable_path='C:\workspaces\workspace_crawling\drivers\chromedriver.exe')

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# 크롬 드라이버 경로 설정, 및 옵션 설정(옵션은 DevToolsActivePort를 찾을 수 없다는 에러 해결을 위해)
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--single-process")
chrome_options.add_argument("--disable-dev-shm-usage")
path = '/home/ubuntu/chromedriver'
driver = webdriver.Chrome(path, options=chrome_options)

url = 'https://sema.seoul.go.kr/kr/whatson/landing'
driver.get(url)
sleep(3)

# 무엇을 체크박스 조작
chk2 = driver.find_element(By.XPATH, '//*[@id="scFrm"]/fieldset/div/div[2]/ul/li[2]/label/span')
chk3 = driver.find_element(By.XPATH, '//*[@id="scFrm"]/fieldset/div/div[2]/ul/li[3]/label/span')
chk2.click()
chk3.click()

# 언제 라디오버튼 조작
rdo_today = driver.find_element(By.XPATH, '//*[@id="scFrm"]/fieldset/div/div[3]/ul/li[1]/label/span')
rdo_past = driver.find_element(By.XPATH, '//*[@id="scFrm"]/fieldset/div/div[3]/ul/li[4]/label/span')

rdo_today.click()
# rdo_past.click()
# 조회하기 버튼 클릭
driver.find_element(By.ID, 'schSubmit').click()

time = datetime.now()
now = time.strftime('%Y%m%d')

## 페이지만큼 가져오기
# 가져와야할 정보
col_list = ['exhibition_id','exhibition_name', 'poster_link', 'exhibition_description', 'exhibition_period', 'exhibition_place']
row_list = []
'''
# 전체 페이지 수 (반복 횟수 지정)
page = driver.find_element(By.XPATH, '//*[@id="contents"]/div[3]/div[2]/div[1]').text
pages = int(page[3:-3].strip())
'''

count = 0
for page in range(1):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    num = soup.select('.c-connected.pure-g > div')
    num = len(num)

    for i in range(0, num):
        try:
            exhibition_id = now + '05' + str(count).zfill(4)
            value_list = []
            poster_link = 'https://sema.seoul.go.kr' + soup.select('.imgexpend')[i]['src']
            exhibition_name = soup.find_all('strong', 'o_h1')[i].text.strip()
            exhibition_period = soup.find_all('span', 'o_h3')[i].text.strip()
            exhibition_place = driver.find_elements(By.CLASS_NAME, 'epEcPlaceNm')[i].text
            desc_path = driver.find_elements(By.CLASS_NAME, 'o_figure')[i]
            desc_path.send_keys(Keys.ENTER)
            sleep(2)
            soup2 = BeautifulSoup(driver.page_source, 'html.parser')
            soup2.find('div', 'o_textmore wordWrap').findChildren('p')
            description_raw = soup2.find('div', 'o_textmore wordWrap').findChildren('p')
            exhibition_description = ' '.join(re.compile('[가-힣]+').findall(str(description_raw)))

        except:
            description_raw = None
            exhibition_description = None
        driver.back()
        sleep(2)

        value_list.append(exhibition_id)
        value_list.append(exhibition_name)
        value_list.append(poster_link)
        value_list.append(exhibition_description)
        value_list.append(exhibition_period)
        value_list.append(exhibition_place)
        row_list.append(value_list)
        count += 1
        #print(exhibition_name, exhibition_description, exhibition_period, exhibition_place, poster_link)


    if driver.find_elements(By.CLASS_NAME, 'direction')[-1].text == '다음':
        driver.find_elements(By.CLASS_NAME, 'direction')[-1].click()
        sleep(2)

    else:
        break

sema_pre_df = pd.DataFrame(row_list, columns=col_list)

sema_pre_df.to_csv(f'~/yogi6/raw_data/crawling/{now}/SEMA.csv', encoding="utf-8-sig", index=False)

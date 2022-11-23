import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

'''
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

response = requests.get(url, headers = headers)

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')
    
print(soup)
'''

url = 'https://sports.news.naver.com/kbaseball/schedule/index'


browser = webdriver.Chrome()
browser.get(url)

xpath_current_month_button = '//*[@id="_currentMonthButton"]'
xpath_month_button_dic = {f'{i}월' : f'//*[@id="_monthList"]/li[{i-2}]/button' for i in range(3, 12)}
current_month_button = browser.find_element(By.XPATH, xpath_current_month_button)
current_month_button.click()

#browser.find_element(By.XPATH, xpath_month_button_dic['4월']).click()


# 경기 일정 (4월)
# xpath_match_button = '//*[@id="calendarWrap"]/div[2]/table/tbody/tr[1]/td[4]/span/a[1]/img'
match_button = browser.find_element(By.XPATH, xpath_match_button)
match_button.click()


# my 티켓 발급하라는 패널 발생하여 취소
xpath_popup_cancel_button = '//*[@id="content"]/div/div/div[3]/div/div[1]/div[1]/div/button'
popup_cancel_button = browser.find_element(By.XPATH, xpath_popup_cancel_button)
popup_cancel_button.click()

# 중계 페이지
xpath_air_button = '//*[@id="content"]/div/div/section[2]/div[1]/ul/li[4]/button'
air_button = browser.find_element(By.XPATH, xpath_air_button)
air_button.click()

# 이닝 선택
html = browser.page_source  # beautifulsoup 사용
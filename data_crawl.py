import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = "https://www.koreabaseball.com/Schedule/Schedule.aspx?seriesId=0,9,6"

'''
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

response = requests.get(url, headers = headers)

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')
    
print(soup)
'''

browser = webdriver.Chrome()
browser.get(url)

xpath_button = '//*[@id="btnReview"]'

# 전체 리뷰(경기) 버튼 list(총 720개 == 팀당 144경기)
button_list = browser.find_elements(By.XPATH, xpath_button)

for i in range(len(button_list)):
    button_list[i].click()
    # time.sleep(3)

    # browser.back()을 두번 해주어야 함.

    browser.back()
    browser.back()

    # browser.execute_script("window.history.go(-2)")
    # time.sleep(3)

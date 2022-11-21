import requests
from bs4 import BeautifulSoup

url = 'https://www.koreabaseball.com/'
postfix = "/Schedule/GameCenter/Main.aspx"#?gameDate=20220402&gameId=20220402HHOB0&section=REVIEW"
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

response = requests.get(url + postfix, headers = headers)

if response.status_code == 200:

    soup = BeautifulSoup(response.content, 'html.parser')
    
print(soup)
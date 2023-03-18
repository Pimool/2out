import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib import parse
from numpy import nan



class Game_data:
    '''
    Game_data Class
    '''
    MAIN_URL = 'http://www.statiz.co.kr/'

    def __init__(self, year):
        self.year = year
        self.__game_url_dict = dict()
        self.__game_id_dict = dict()
        self.__game_num = 0
        for i in self.__url_month(self.year).values():
            for j in self.__url_schedule(i).values():
                for k in j:
                    self.__game_num += 1
                    game_id = f'{self.year}_{str(self.__game_num).zfill(3)}'
                    self.__game_url_dict[game_id] = k[:37] + 'opt=5&' + k[37:]
                    self.__game_id_dict[k[:37] + 'opt=5&' + k[37:]] = game_id
        self.game_id_dict = self.__game_id_dict



    def get_game_month(self, month):
        return self.__url_schedule(self.__url_month(self.year)[f'{month}월'])

    def get_gameurl(self, game_id):
        return self.__url_gamelog(self.__game_url_dict[game_id])

    def get_gameid(self, game_log_url : str):
        return self.__game_id_dict[game_log_url]

    def get_data(self, game_id):
        game_url = self.__game_url_dict[game_id]
        log_url = self.__url_gamelog(game_url)
        result = self.__game_result(log_url)
        return self.__preprocess(result)
    
    def get_info(self, game_id):
        game_url = self.__game_url_dict[game_id]
        log_url = self.__url_gamelog(game_url)
        return self.__game_info(log_url)
    
    def to_xlsx(self, game_id : str):
        df_game_data = self.get_data(game_id)
        df_game_info = self.get_info(game_id)
        writer= pd.ExcelWriter(f'{game_id}.xlsx', engine = 'xlsxwriter')
        df_game_data.to_excel(writer, sheet_name = '경기내용', encoding = 'euc-kr', index = False)
        df_game_info.to_excel(writer, sheet_name = '경기정보', encoding = 'euc-kr', index = False)
        writer.close()

    def merge(self, start = 1, end = None):
        if end is None:
            end = self.__game_num

        if start > end:
            raise ValueError

        df_game_data = pd.DataFrame({}, columns = ['경기id', '이닝', '투수', '타순', '타자', 'P', '결과', '이전상황', '이후상황', 'LEV', 'REs', 'REa', 'WPe', 'WPa'])
        df_game_info = pd.DataFrame({}, columns = ['경기id', '날짜', '시간', '경기장', '홈팀', '원정팀', '점수', '스탯티즈 url'])
        for i in range(start, end + 1):
            df_game_data = pd.concat([df_game_data, self.get_data(f'{self.year}_{str(i).zfill(3)}')])
            df_game_info = pd.concat([df_game_info, self.get_info(f'{self.year}_{str(i).zfill(3)}')])

        writer= pd.ExcelWriter(f'{self.year}_{str(start).zfill(3)}~{self.year}_{str(end).zfill(3)}.xlsx', engine = 'xlsxwriter')
        df_game_data.to_excel(writer, sheet_name = '경기내용', encoding = 'euc-kr', index = False)
        df_game_info.to_excel(writer, sheet_name = '경기정보', encoding = 'euc-kr', index = False)
        writer.close()

# -------------------------------------------------------------------------------------------------------------------

    def __url_month(self, year) -> dict:
        month_dic = dict()
        for i in range(4, 12):
            month_dic[f'{i}월'] = f'http://www.statiz.co.kr/schedule.php?opt={i}&sy={year}'
        return month_dic


    def __url_schedule(self, month_url : str) -> dict:
        r = requests.get(
                url = month_url,
                headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
                }
            )

        soup = BeautifulSoup(r.content, 'html.parser')
        schedule_table = soup.find('table', {'class' : 'table table-striped table-bordered'})
        day_cell = schedule_table.find_all('div', {'class' : 'hidden-md hidden-sm hidden-lg'})

        schedule_dict = dict()
        # 월요일 경기 없을 수 있음 -> 없는 날은 try except문
        for i in range(len(day_cell)):
            schedule_dict[f'{i+1}일'] = list()
            try:
                for x in day_cell[i].find_all('a'):
                    schedule_dict[f'{i+1}일'].append(self.MAIN_URL + x['href'])
            except:
                pass
        
        return schedule_dict


    def __url_gamelog(self, url : str) -> str:
        '''
        ex)
        input : 'boxscore.php?date=2022-04-02&stadium=%EA%B3%A0%EC%B2%99%EB%8F%94&hour=14'
        output : 'boxscore.php?opt=5&date=2022-04-02&stadium=%EA%B3%A0%EC%B2%99%EB%8F%94&hour=14'
        -> 사실 opt=5만 붙이면 됨
        '''
        r = requests.get(
            url = url,
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
            }
        )
        soup = BeautifulSoup(r.content, 'html.parser')
        game_log_url = soup.find_all('a', {'class' : 'btn btn-app swipeclass'})[4]['href']
        return self.MAIN_URL + game_log_url


    def __game_result(self, game_log_url : str):

        r = requests.get(
            url = game_log_url,
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
            }
        )
        soup = BeautifulSoup(r.content, 'html.parser')
        gamelog_table = soup.find_all('table', {'class' : 'table table-striped'})[2]


        df_game_data = pd.DataFrame({}, columns = ['이닝', '투수', '타자', 'P', '결과', '이전상황', '이후상황', 'LEV', 'REs', 'REa', 'WPe', 'WPa'])

        for j in gamelog_table.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            df_game_data.loc[len(df_game_data)] = row

        df_game_data['경기id'] = self.get_gameid(game_log_url)

        return df_game_data


    def __preprocess(self, df_game_data : pd.DataFrame) -> pd.DataFrame:
        
        df_game_data['이닝'] = df_game_data['이닝'].apply(lambda x : nan if x == '' else x)
        df_game_data['이닝'] = df_game_data['이닝'].ffill()
        df_game_data['타순'] = df_game_data['타자'].str.split(' ').str[0]
        df_game_data['타자'] = df_game_data['타자'].str.split(' ').str[1]
        df_game_data['결과'] = df_game_data.apply(lambda x: x['결과'][len(x['타자'])+3:] if (x['결과'].startswith(x['타자']) and x['타자'] != '') else x['결과'], axis = 1)
        
        df_game_data = df_game_data[['경기id', '이닝', '투수', '타순', '타자', 'P', '결과', '이전상황', '이후상황', 'LEV', 'REs', 'REa', 'WPe', 'WPa']]

        return df_game_data


    def __game_info(self, game_log_url : str):

        r = requests.get(
            url = game_log_url,
            headers = {
                'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
            }
        )
        soup = BeautifulSoup(r.content, 'html.parser')

        game_id = self.get_gameid(game_log_url)
        home_team = soup.find_all('h3', {'class' : 'box-title'})[2].text[:-5]
        away_team = soup.find_all('h3', {'class' : 'box-title'})[1].text[:-5]
        day = game_log_url[re.search(r'date=[0-9-]+', game_log_url).start()+5 : re.search(r'date=[0-9-]+', game_log_url).end()]
        time = game_log_url[re.search(r'hour=[0-9]+', game_log_url).start()+5 : re.search(r'hour=[0-9]+', game_log_url).end()]
        score = soup.find('div', {'class' : 'callout'}).text
        score = score[re.search(r'[0-9]+ : [0-9]+', score).start() : re.search(r'[0-9]+ : [0-9]+', score).end()]
        stadium = parse.unquote(game_log_url[re.search(r'stadium=[A-Z0-9%+]+', game_log_url).start()+8 : re.search(r'stadium=[A-Z0-9%+]+', game_log_url).end()])
        stadium = stadium.replace('+', ' ')

        df = pd.DataFrame({
            '경기id' : [game_id],
            '날짜' : [day],
            '시간' : [time],
            '경기장' : [stadium],
            '홈팀' : [home_team],
            '원정팀' : [away_team],
            '점수' : [score],
            '스탯티즈 url' : [self.MAIN_URL + game_log_url]
        })
        
        return df




if __name__ == '__main__':
    print('hi')
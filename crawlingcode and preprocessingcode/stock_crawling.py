# 오늘의 날짜를 가져온다.
import pandas as pd
import datetime
import numpy as np
import time
import os
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

# 주식 데이터 크롤링
def stock_crawling(sosok,market,per_page):
    for page in range(1,per_page):
        url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok='+str(sosok)+'&page='+str(page)
        result = requests.get(url)
        soup = BeautifulSoup(result.content,'html.parser')

        stock_table = soup.find("table",{"class":"type_2"})
        summary_stock = stock_table.find('tbody')
        data_list = summary_stock.find_all('tr')
        data_list = data_list[1:]

        # tmp 리스트에 tr 데이터의 공백을 제거하고 append를 한다.
        tmp = list()
        for tr_data in data_list:
            for i in tr_data:
                try:
                    preprocessing = i.text.strip()
                    if preprocessing != '':
                        tmp.append(i.text.strip())
                except:
                    pass

        # 들어온 데이터는 12개씩 하나의 tr에서 온 데이터다. 각각의 데이터들의 인덱스를 활용하여
        # 해당하는 리스트에 append 해준다.
        index = 0
        for i in tmp:
            if index%12 == 0:
                ranking_list.append(i)
                index+=1

            elif index%12 == 1:
                company_list.append(i)
                index+=1

            elif index%12 == 2:
                price_list.append(i)
                index+=1

            elif index%12 == 3:
                per_yesterday_list.append(i)
                index+=1

            elif index%12 == 4:
                indecrese_list.append(i)
                index+=1

            elif index%12 == 5:
                acmyeonga_list.append(i)
                index+=1

            elif index%12 == 6:
                siga_total_list.append(i)
                index+=1

            elif index%12 == 7:
                sangjang_stock_list.append(i)
                index+=1

            elif index%12 == 8:
                foreign_part_list.append(i)
                index+=1

            elif index%12 == 9:
                perstock_list.append(i)
                index+=1

            elif index%12 == 10:
                per_list.append(i)
                index+=1

            elif index%12 == 11:
                roe_list.append(i)
                index+=1

        # tr의 갯수만큼 날짜와 시간, 주식시장을 리스트에 넣어준다.
        for i in range(int(len(tmp)/12)):
            date_list.append(today)
            time_list.append(time)
            market_list.append(market)

if __name__ == "__main__":
    # 오늘의 날짜와 시간을 가져온다.
    todays_date = datetime.datetime.now()
    today = str(todays_date.year) +'-'+ str(todays_date.month)+'-'+str(todays_date.day)
    time = str(todays_date.hour)+':'+str(todays_date.minute)

    # 코스피 목록의 마지막 페이지 넘버를 알아낸다.
    driver1 = webdriver.Chrome('C:\\Users\\HyunMok\\Desktop\\projectforhadoop\\chromedriver_win32\\chromedriver.exe')
    driver1.get('https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0')
    # 맨 마지막 페이지를 클릭한다.
    driver1.find_element_by_css_selector('#contentarea > div.box_type_l > table.Nnavi > tbody > tr > td.pgRR > a').click()
    # url에서 'page=' 뒤에 있는 숫자를 슬라이싱으로 가져온다.
    reference_num = driver1.current_url.find('page=')
    last_num_kospi = int(driver1.current_url[reference_num+5:])

    driver1.close()

    # 코스닥 목록의 마지막 페이지 넘버를 알아낸다.
    driver2 = webdriver.Chrome('C://Users//HyunMok//Desktop//projectforhadoop//chromedriver_win32//chromedriver.exe')
    driver2.get('https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1')
    # 맨 마지막 페이지를 클릭한다.
    driver2.find_element_by_css_selector('#contentarea > div.box_type_l > table.Nnavi > tbody > tr > td.pgRR > a').click()
    # url에서 'page=' 뒤에 있는 숫자를 슬라이싱으로 가져온다.
    reference_num2 = driver2.current_url.find('page=')
    last_num_kosdac = int(driver2.current_url[reference_num+5:])

    driver2.close()

    # 필요한 변수 선언
    date_list = list()
    time_list = list()
    ranking_list = list()
    market_list = list()
    company_list = list()
    price_list = list()
    per_yesterday_list = list()
    indecrese_list = list()
    acmyeonga_list = list()
    siga_total_list = list()
    sangjang_stock_list = list()
    foreign_part_list = list()
    perstock_list = list()
    per_list = list()
    roe_list = list()

    # 크롤링 함수로 크롤링을 실행한다.
    stock_crawling(0,'코스피',last_num_kospi+1)
    stock_crawling(1,'코스닥',last_num_kosdac+1)

    # 최종 데이터 프레임을 만들고 데이터를 넣는다.
    today_stock_list = {'날짜':date_list,"시간":time_list,"시장":market_list,'NO':ranking_list,"종목명":company_list,"현재가":price_list,"전일비":per_yesterday_list,
                    "등락률":indecrese_list,"액면가":acmyeonga_list,'시가총액':siga_total_list,'상장주식수':sangjang_stock_list,'외국인비율':foreign_part_list,
                    '거래량':perstock_list,'PER':per_list,'ROE':roe_list}
    today_summary = pd.DataFrame(today_stock_list)

    # 데이터프레임을 csv와 excel로 저장한다.
    # 2가지 파일 형태로 저장하는 이유 - csv로 저장시 한글이 깨질 수도 있음 -> 만약 csv에서 한글이 깨질경우
    # 엑셀파일을 이용하기 위해 2가지 파일로 저장함
    today_summary.to_excel('stock_'+str(todays_date.year) + str(todays_date.month)+str(todays_date.day)+'_'+str(todays_date.hour)+'시'+str(todays_date.minute)+'분'+'.xlsx')
    today_summary.to_csv('stock_'+str(todays_date.year) + str(todays_date.month)+str(todays_date.day)+'_'+str(todays_date.hour)+'시'+str(todays_date.minute)+'분'+'.csv')
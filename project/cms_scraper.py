import os
import sys
import time

from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains

''' URL 정보
역별 승하자 인원 정보
https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do

역별 시간대별 승하차 인원 정보
https://data.seoul.go.kr/dataList/OA-12252/S/1/datasetView.do
'''


line_name = "1호선"


def sol_subway_traffic_daily():
    '''
    승하차 인원 정보 URL : onandoff_info_url

    해당 사이트의 dropdown, 필드명 검색 태그 관련 text
    dropdown_id = selt_filterCol
    dropdown_id_option_value = LINE_NUM
    
    검색명 input tag xpath = //*[@id="txtFilter"]

    조회 버튼 xpath = //*[@id="frmSheet"]/div[3]/button[3]

    테이블 6개, columns = f'//*[@id="AXGridTarget_AX_colHead_AX_0_AX_{i}"]'
    
    j = row별, i = row내 column 순서
    테이블 rows = f'//*[@id="AXGridTarget_AX_bodyText_AX_0_AX_{j}_AX_{i}"]'
    
    '''

    driver = webdriver.Chrome('project\chromedriver.exe')
    df = pd.DataFrame()

    info_url_onandoff = "https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do"
    to_preparation(driver, info_url_onandoff)
    ''' to_preparation
    # driver.get(info_url_onandoff)
    # driver.implicitly_wait(3)

    # dropdown = Select(driver.find_element(By.XPATH, '//*[@id="selt_filterCol"]'))
    # dropdown.select_by_value("LINE_NUM")

    # # 검색명 input tag 입력
    # driver.find_element(By.XPATH, '//*[@id="txtFilter"]').send_keys(line_name)
    # driver.implicitly_wait(3)

    # # 조회 버튼 클릭
    # driver.find_element(By.XPATH, '//*[@id="frmSheet"]/div[3]/button[3]').click()
    # driver.implicitly_wait(5)
    '''
    time.sleep(3)

    ''' cloumns 정의
    # columns = list()
    # for i in range(6):
    #     colHead = driver.find_element(By.XPATH, f'//*[@id="AXGridTarget_AX_colHead_AX_0_AX_{i}"]')
    #     driver.implicitly_wait(2)
    #     # df.columns[i] = colHead.text
    #     # []'사용일자\nT', '호선명\nT', '역명\nT', '승차총승객수\nT', '하차총승객수\nT', '등록일자']
    #     columns.append(colHead.text.split('\n')[0])
    '''
    columns = ['date', 'line', 'station_name', 'people_in', 'people_out', 'upload_date']


    # df rows 정의
    df = pd.DataFrame()

    for _ in range(20):
        html = driver.page_source
        df_data = pd.read_html(html, header=0, encoding='utf-8')[5].iloc[1:-1,:-1]
        df = pd.concat([df, df_data], axis=0, ignore_index=False, join='outer')

        # 스크롤 위치 변경
        scroll = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')
        ActionChains(driver).click_and_hold(scroll).perform()
        ActionChains(driver).move_by_offset(0, 10).perform()
        ActionChains(driver).release(scroll).perform()
        driver.implicitly_wait(5)

    # 컬럼명 추가
    df.columns = columns

    # tmp name df1으로 정의, 전처리
    df1 = df

    df1 = df1.reset_index(drop=True)
    drop_another_columns = df1[df1['line'] == '공항철도 1호선'].index
    df1.drop(drop_another_columns, inplace=True)
    df1 = df1.drop('upload_date', axis=1)
    print(df1)
    df1 = df1.reset_index(drop=True)
    df1.drop_duplicates(keep='first', ignore_index=True, inplace=True)

    df1['date'] = pd.to_datetime(df1['date'], format='%Y%m%d', errors='raise')
    df1['people_in'] = df1['people_in'].astype('int64')
    df1['people_out'] = df1['people_out'].astype('int64')
    
    df1.to_csv('subway_traffic_daily.csv', mode='w')
    return




def sol_subway_traffic_month_hourly():
    driver = webdriver.Chrome('chromedriver')
    df = pd.DataFrame()

    info_url_onandoff = "https://data.seoul.go.kr/dataList/OA-12252/S/1/datasetView.do"
    to_preparation(driver, info_url_onandoff)
    ''' to_preparation
    # info_url_onandoff = "https://data.seoul.go.kr/dataList/OA-12252/S/1/datasetView.do"
    # driver.get(info_url_onandoff)
    # driver.implicitly_wait(3)

    # dropdown = Select(driver.find_element(By.XPATH, '//*[@id="selt_filterCol"]'))
    # dropdown.select_by_value("LINE_NUM")

    # # 검색명 input tag 입력
    # driver.find_element(By.XPATH, '//*[@id="txtFilter"]').send_keys(line_name)
    # driver.implicitly_wait(3)

    # # 조회 버튼 클릭
    # driver.find_element(By.XPATH, '//*[@id="frmSheet"]/div[3]/button[3]').click()
    # driver.implicitly_wait(5)
    '''
    # 정렬 기준 호선명 2번 클릭으로 1호선을 상위로
    line_sort = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_colHead_AX_0_AX_1"]')
    # NONE-> DESC -> ACS
    ActionChains(driver).click(line_sort).perform()
    ActionChains(driver).click(line_sort).perform()
    time.sleep(3)

    # rows
    html = driver.page_source
    df = pd.read_html(html)[5].iloc[1:-1,:-1]

    # columns
    columns = []
    for c in pd.read_html(html)[4].loc[0]:
        columns.append(c.rstrip('T'))

    df.columns = columns
    df.rename(columns={'사용월':'month', '호선명':'line', '지하철역':'station_name'}, inplace=True)
    df.drop('작업일자', axis=1, inplace=True)
    df['month'] = pd.to_datetime(df['month'], format='%Y%m', errors='raise') # format 수정필요, 현재 : 2023-03-01

    for c in df.iloc[[],3:]:
        df[c] = df[c].astype('int64')


    df.to_csv('subway_traffic_month_hourly.csv', mode='w')
    return 





def to_preparation(driver, url):
    driver.get(url)
    driver.implicitly_wait(3)

    dropdown = Select(driver.find_element(By.XPATH, '//*[@id="selt_filterCol"]'))
    dropdown.select_by_value("LINE_NUM")

    # 검색명 input tag 입력
    driver.find_element(By.XPATH, '//*[@id="txtFilter"]').send_keys(line_name)
    driver.implicitly_wait(3)

    # 조회 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="frmSheet"]/div[3]/button[3]').click()
    driver.implicitly_wait(5)



def main():
    sol_subway_traffic_daily()
    sol_subway_traffic_month_hourly()

    return

if __name__ == "__main__":
    main()
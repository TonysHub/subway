#!/usr/bin/env python
# coding: utf-8
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.ui import Select 
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# ## subway_traffic_daily
def subway_traffic_daily():
    # 서울시 지하철 호선별 역별 승하차 인원 정보 요청보내기
    driver.get("https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do")
    time.sleep(1)

    #필터 클릭
    button = driver.find_element(By.ID, "selt_filterCol")
    ActionChains(driver).click(button).perform() # filter 열기
    time.sleep(0.5)


    # 호선명 클릭
    button.send_keys('호선명')
    button.send_keys(Keys.RETURN)

    # 검색명에 '2호선' 입력
    search_field = driver.find_element(By.XPATH, '//*[@id="txtFilter"]')
    ActionChains(driver).send_keys_to_element(search_field, "2호선").perform()
    ActionChains(driver).scroll_by_amount(0, 500).perform()
    time.sleep(1)

    # 조회 버튼 클릭
    search_click = driver.find_element(By.XPATH, '//*[@id="frmSheet"]/div[3]/button[3]/span')
    ActionChains(driver).click(search_click).perform()
    time.sleep(1)

    # 데이터 
    df = []
    data = pd.DataFrame()
    for i in range(60): #3
        html = driver.page_source
        df = pd.read_html(html)[5].iloc[1:-1,:-1]
        data = pd.concat([data, df], axis=0)
        time.sleep(0.3)
        scroll = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')
        ActionChains(driver).click_and_hold(scroll).perform()
        ActionChains(driver).move_by_offset(0,5).perform()
        ActionChains(driver).release(scroll).perform()
        
    # 전처리
    # 컬럼명 변경
    data.columns = ['date', 'line', 'station_name', 'people_in', 'people_out', 'upload_date']
    data = data.reset_index(drop=True) # 인덱스 다시 부여
    time.sleep(1)

    d = data
    d['people_in'] = d['people_in'].astype(int)
    d['people_out'] = d['people_out'].astype(int)
    d['date'] = d['date'].astype(int)
    d['date'] = pd.to_datetime(d['date'], format='%Y%m%d')
    d['upload_date'] = d['upload_date'].astype(int)
    d['upload_date'] = pd.to_datetime(d['upload_date'], format='%Y%m%d')

    return d

# ## subway_traffic_month_hourly
def subway_traffic_month_hourly():
    # 서울시 지하철호선별 역별 시간대별 승하차 인원 정보 요청보내기
    driver.get("https://data.seoul.go.kr/dataList/OA-12252/S/1/datasetView.do")
    time.sleep(1)

    #필터 클릭
    button = driver.find_element(By.ID, "selt_filterCol")
    ActionChains(driver).click(button).perform() # filter 열기
    time.sleep(0.5)


    # 호선명 클릭
    button.send_keys('호선명')
    button.send_keys(Keys.RETURN)

    # 검색명에 '2호선' 입력
    search_field = driver.find_element(By.XPATH, '//*[@id="txtFilter"]')
    ActionChains(driver).send_keys_to_element(search_field, "2호선").perform()
    ActionChains(driver).scroll_by_amount(0, 500).perform()
    time.sleep(1)

    # 조회 버튼 클릭
    search_click = driver.find_element(By.XPATH, '//*[@id="frmSheet"]/div[3]/button[3]/span')
    ActionChains(driver).click(search_click).perform()
    time.sleep(1.5)

    # 데이터
    df = []
    data = pd.DataFrame()
    for i in range(11): #3
        html = driver.page_source
        df = pd.read_html(html)[5].iloc[1:-1,:-1]
        data = pd.concat([data, df], axis=0)
        time.sleep(0.3)
        scroll = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')
        ActionChains(driver).click_and_hold(scroll).perform()
        ActionChains(driver).move_by_offset(0,5).perform()
        ActionChains(driver).release(scroll).perform()

    # 전처리
    # 컬럼명 추출
    c_list = []
    i = 0
    for _ in range(26):
        for _ in range(2):
            x = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_colHeadText_AX_0_AX_{}"]'.format(i))
            c_list.append(x.text)
            i += 1
            time.sleep(0.5)

        scroll_x = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollXHandle"]')
        ActionChains(driver).click_and_hold(scroll_x).perform()
        ActionChains(driver).move_by_offset(32,0).perform()
        ActionChains(driver).release(scroll_x).perform()
        
    # 컬럼명 변경
    data.columns = [i for i in c_list]
    data = data.reset_index(drop=True) # 인덱스 다시 부여

    #데이터 타입 변경
    d2 = data
    d2['사용월'] = pd.to_datetime(d2['사용월'], format='%Y%m')
    d2['작업일자'] = d2['작업일자'].astype(int)
    d2['작업일자'] = pd.to_datetime(d2['작업일자'], format='%Y%m%d')
    for i in range(3, 52):
        if d2[c_list[i]].dtype == 'float64':
            d2[c_list[i]] = d2[c_list[i]].astype(int)
    
    return d2

daily = subway_traffic_daily()
hourly = subway_traffic_month_hourly()
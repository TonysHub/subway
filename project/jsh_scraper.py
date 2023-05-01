from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

import pandas as pd
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import time


def get_data(url, line_name):
    """ url(str) 과 line_name(str)을 입력받아 해당하는 웹 사이트에서 원하는 line_name만 필터링하여 데이터를 추출하여 dataframe형식으로 반환하는 함수입니다.
    
        url :
            서울시 지하철호선별 역별 승하차 인원 정보 :
                "https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do"
            
            서울시 지하철 호선별 역별 시간대별 승하차 인원 정보 :
                "https://data.seoul.go.kr/dataList/OA-12252/S/1/datasetView.do"
                
        line_name:
            '2호선' '1호선' '4호선' '7호선' '3호선'

        
        1. 해당 url로 접속하여 미리보기sheet까지 이동하기
        2. 미리보기 sheet에서 스크롤을 내려가며 필터링된 데이터 추출하고 병합하기
        3. 병합된 최종 데이터프레임을 날짜형식과 숫자, 문자열에 맞게 수정하기
        
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    # options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    
    
    # 1. 해당 url로 접속하여 미리보기sheet까지 이동하기
    driver.get(url)
    driver.implicitly_wait(20)
    filterCol = driver.find_element(By.XPATH,'//*[@id="selt_filterCol"]')

    field_name =Select(filterCol)
    field_name.select_by_value("LINE_NUM")
    driver.implicitly_wait(2)

    txtFilter = driver.find_element(By.XPATH, '//*[@id="txtFilter"]')
    ActionChains(driver).send_keys_to_element(txtFilter,line_name).perform()
    driver.implicitly_wait(2)

    btn_search = driver.find_element(By.XPATH, '//*[@id="frmSheet"]/div[3]/button[3]/span')
    ActionChains(driver).click(btn_search).perform()
    driver.implicitly_wait(3)

    elem = driver.find_element(By.XPATH, '//*[@id="datasetSeetView"]')
    ActionChains(driver).move_to_element(elem).perform()
    time.sleep(2)
    
    
    # 2. 미리보기 sheet에서 스크롤을 내려가며 필터링된 데이터 추출하고 병합하기
    result_df = pd.DataFrame()
    while(True):
        html = driver.page_source
        df = pd.read_html(html)[5].iloc[1:-1,:-1]
        result_df = pd.concat([df, result_df]).drop_duplicates([0,2]).dropna()
        top = str(driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]').get_attribute('style')).split(' ')[-1]
        scroll = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')
        ActionChains(driver).click_and_hold(scroll).perform()
        
        # 미리보기 sheet의 가장 아래 위치는 375px 이며, 이보다 더 낮은 값은 들어올 수 없다
        if top == '375px;' :
            print('len(result_df) : ',len(result_df))
            break
        
        # 현재 미리보기sheet의 스크롤을 10px 아래로 내린다
        ActionChains(driver).move_by_offset(0,10).perform()
        ActionChains(driver).release(scroll).perform()
        driver.implicitly_wait(1) 

    print('finish scrapying :D' )
    
    
    # 3. 병합된 최종 데이터프레임을 날짜형식과 숫자, 문자열에 맞게 수정하기
    result_df.columns = pd.read_html(html)[4].iloc[0,:].str.replace('T','')    
    if result_df.columns[0] == '사용일자' :
        result_df['사용일자'] = pd.to_datetime(result_df['사용일자'], format='%Y%m%d')
        result_df['등록일자'] = pd.to_datetime(result_df['등록일자'], format='%Y%m%d')   
        result_df[result_df.columns[3:-1]] = result_df[result_df.columns[3:-1]].astype(int)
        
        
    elif result_df.columns[0] == '사용월' :
        result_df['사용월'] = pd.to_datetime(result_df['사용월'], format='%Y%m')
        result_df['작업일자'] = pd.to_datetime(result_df['작업일자'], format='%Y%m%d')   
        result_df[result_df.columns[3:-1]] = result_df[result_df.columns[3:-1]].astype(int)
        
        
        
    return result_df



result1 = get_data("https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do",'7호선')
result2 = get_data("https://data.seoul.go.kr/dataList/OA-12252/S/1/datasetView.do",'7호선')

import datetime
import time
import pandas as pd
import numpy as np

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def subway_traffic_daily(line_name):
    url = "https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do"
    driver = get_driver(url)

    # data sheet 준비
    move_to_data(driver, line_name)


    # columns
    columns_list = ['date', 'line', 'station', 'people_in', 'people_out', 'upload_date']

    # rows
    current_date = datetime.datetime.now().date()
    deadline = current_date - datetime.timedelta(days=15)

    df_std = pd.DataFrame() # subway_traffic_daily -> std
    mouse_tracker = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')


    while True:
        html = driver.page_source
        driver.implicitly_wait(5)

        df = pd.read_html(html, encoding='utf-8')[5].iloc[1:-1,:-1]
        time.sleep(0.2)

        upload_date = datetime.datetime.strptime(str(df[5].iloc[-1]).replace('.0',''), '%Y%m%d').date() # df[5] -> upload_date
        df_std = pd.concat([df_std, df])
        time.sleep(0.1)

        # print(current_date, upload_date, deadline) # check date
        if current_date >= upload_date > deadline:
            ActionChains(driver).move_to_element_with_offset(mouse_tracker, 0, 0).click_and_hold().move_by_offset(0,6).perform()
            driver.implicitly_wait(0.5)
        else:
            break
        
    


    # 데이터 전처리
    df_std.columns = columns_list
    df_std.drop('upload_date', axis=1, inplace=True)
    df_std.drop_duplicates(keep='first', inplace=True)
    df_std.reset_index(drop=True, inplace=True)
    time.sleep(0.1)

    df_std[['line', 'station']] = df_std[['line', 'station']].astype('str')
    df_std[['people_in', 'people_out']] = df_std[["people_in", "people_out"]].astype('int64')
    df_std['date'] = pd.to_datetime(df_std['date'], format='%Y%m%d', errors='raise')

    # 14일 이전을 넘어가는 데이터 삭제
    deadline = df_std['date'][0].date() - datetime.timedelta(days=14)
    df_std = df_std[df_std['date'].between(str(deadline), str(df_std['date'][0].date()))]


    # df_std.to_csv('subway_traffic_daily.csv', mode='w')

    return df_std



def subway_traffic_month_hourly(line_name):
    url = "https://data.seoul.go.kr/dataList/OA-12252/S/1/datasetView.do"
    driver = get_driver(url)

    # data sheet 준비
    move_to_data(driver, line_name)


    # columns
    html = driver.page_source
    columns_list = pd.read_html(html)[4]
    columns_list = columns_list.squeeze().tolist()
    columns_list = list(map(lambda x: x.replace('T', ''), columns_list))

    # rows
    current_date = datetime.datetime.now().date()
    deadline = datetime.datetime
    if current_date.day > 3:
        deadline = current_date - relativedelta(months=4)
    else:
        deadline = current_date - relativedelta(months=5)

    df_stmh = pd.DataFrame() # subway_traffic_month_hourly -> stmh
    mouse_tracker = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')   

    while True:
        html = driver.page_source
        driver.implicitly_wait(5)
        time.sleep(0.1)


        df = pd.read_html(html, encoding='utf-8')[5].iloc[1:-1,:-1]
        time.sleep(0.2)

        month_date = datetime.datetime.strptime(str(df[0].iloc[-1]).replace('.0',''), '%Y%m').date() # df[0] -> month
        df_stmh = pd.concat([df_stmh, df])
        time.sleep(0.1)
        
        print(current_date , month_date , deadline)
        if current_date > month_date > deadline:
            ActionChains(driver).move_to_element_with_offset(mouse_tracker, 0, 0).click_and_hold().move_by_offset(0,6).perform()
            driver.implicitly_wait(0.5)
        else:
            break


    # 데이터 전처리
    df_stmh.columns = columns_list
    df_stmh.drop_duplicates(keep='first', inplace=True)
    df_stmh.reset_index(drop=True, inplace=True)

    df_stmh.drop('작업일자', axis=1, inplace=True)
    df_stmh.rename(columns={'사용월':'month', '호선명':'line', '지하철역':'station'}, inplace=True)
    df_stmh['month']=pd.to_datetime(df_stmh["month"], format='%Y%m').dt.strftime("%Y-%m")

    df_stmh = df_stmh.apply(lambda x: x.astype('int64') if x.dtype == 'float64' else x)

    # 3개월 이전을 넘어가는 데이터 삭제
    deadline += relativedelta(months=1)
    df_stmh = df_stmh[df_stmh['month'].between(str(deadline)[:7], df_stmh["month"][0])]

    # df_stmh.to_csv('subway_traffic_month_hourly.csv', mode='w')

    return df_stmh


def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get(url)
    driver.implicitly_wait(10)


    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="AXGridTarget_AX_tbody"]')))

    return driver


def move_to_data(driver, line_name):
    # dropdown filter를 호선명 클릭
    # dropdown = Select(driver.find_element(By.XPATH, '//*[@id="selt_filterCol"]'))
    dropdown = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="selt_filterCol"]'))))

    driver.find_element(By.NAME, 'filterCol')
    driver.implicitly_wait(5)

    dropdown.select_by_value("LINE_NUM")
    driver.implicitly_wait(5)

    time.sleep(0.2)


    # 검색명 input tag 입력
    driver.find_element(By.XPATH, '//*[@id="txtFilter"]').send_keys(line_name)
    driver.implicitly_wait(5)
    time.sleep(0.2)

    # 조회 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="frmSheet"]/div[3]/button[3]').click()
    driver.implicitly_wait(10)
    time.sleep(1)

    # 1호선의 경우 '공항철도 1호선' 이 포함되는 것에 대한 예외 if
    if line_name=='1호선':
        # column 클릭마다 정렬 기준 변경 process, recent -> DESC -> ACS 
        line_sort = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_colHead_AX_0_AX_1"]')
        ActionChains(driver).click(line_sort).perform()
        ActionChains(driver).click(line_sort).perform()
        driver.implicitly_wait(3)
        time.sleep(0.2)

    return driver



def main():
    lines = ['1호선', '2호선', '3호선',' 4호선', '7호선']
    now = datetime.datetime.now().day

    df_std = pd.DataFrame()
    df_stmh = pd.DataFrame()
    
    for line in lines:
        df1 = subway_traffic_daily(line)
        df_std = pd.concat([df_std, df1])
        time.sleep(0.2)

        # if now == 4: # 매월 4일마다 갱신
        df2 =subway_traffic_month_hourly(line)
        df_stmh = pd.concat([df_stmh, df2])
        time.sleep(0.2)



    df_std.to_csv('subway_traffic_daily.csv', mode='w')
    df_stmh.to_csv('subway_traffic_month_hourly.csv', mode='w')

    # return df_std, df_stmh

    pass

if __name__ == "__main__":
    main()
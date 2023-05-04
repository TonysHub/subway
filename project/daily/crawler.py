import datetime
import time
import pandas as pd
import os.path

from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.select import Select

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

    df_subway_traffic_daily = pd.DataFrame() # subway_traffic_daily -> std
    mouse_tracker = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')


    while True:
        html = driver.page_source
        driver.implicitly_wait(5)
        time.sleep(0.1)

        df = pd.read_html(html, encoding='utf-8')[5].iloc[1:-1,:-1]
        time.sleep(0.05)

        upload_date = datetime.datetime.strptime(str(df[5].iloc[-1]).replace('.0',''), '%Y%m%d').date() # df[5] -> upload_date
        df_subway_traffic_daily = pd.concat([df_subway_traffic_daily, df])
        time.sleep(0.05)

        # print(current_date, upload_date, deadline) # check date
        if current_date >= upload_date > deadline:
            ActionChains(driver).move_to_element_with_offset(mouse_tracker, 0, 0).click_and_hold().move_by_offset(0,6).perform()
            driver.implicitly_wait(0.5)
        else:
            break
        
    


    # 데이터 전처리
    df_subway_traffic_daily.columns = columns_list
    df_subway_traffic_daily.drop('upload_date', axis=1, inplace=True)
    df_subway_traffic_daily.drop_duplicates(keep='first', inplace=True)
    df_subway_traffic_daily.reset_index(drop=True, inplace=True)
    time.sleep(0.1)

    df_subway_traffic_daily[['line', 'station']] = df_subway_traffic_daily[['line', 'station']].astype('str')
    df_subway_traffic_daily[['people_in', 'people_out']] = df_subway_traffic_daily[["people_in", "people_out"]].astype('int64')
    df_subway_traffic_daily['date'] = pd.to_datetime(df_subway_traffic_daily['date'], format='%Y%m%d', errors='raise')

    # 14일 이전을 넘어가는 데이터 삭제
    deadline = df_subway_traffic_daily['date'][0].date() - datetime.timedelta(days=14)
    df_subway_traffic_daily = df_subway_traffic_daily[df_subway_traffic_daily['date'].between(str(deadline), str(df_subway_traffic_daily['date'][0].date()))]


    # df_subway_traffic_daily.to_csv('subway_traffic_daily.csv', mode='w')

    return df_subway_traffic_daily



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
    for i, column in enumerate(columns_list):
        if '승차' in column:
            columns_list[i] = 'in_'+column[:2]+column[4:6]
        elif '하차' in column:
            columns_list[i] = 'out_'+column[:2]+column[4:6]


    # rows
    current_date = datetime.datetime.now().date()
    
    deadline = datetime.datetime
    if current_date.day > 3:
        deadline = current_date - relativedelta(months=4)
    else:
        deadline = current_date - relativedelta(months=5)

    df_subway_traffic_month_hourly = pd.DataFrame() # subway_traffic_month_hourly -> stmh
    mouse_tracker = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')   
    driver.implicitly_wait(3)
    time.sleep(2)
    
    while True:
        html = driver.page_source
        driver.implicitly_wait(10)
        time.sleep(0.1)


        df = pd.read_html(html, encoding='utf-8')[5].iloc[1:-1,:-1]
        time.sleep(0.2)

        month_date = datetime.datetime.strptime(str(df[0].iloc[-1]).replace('.0',''), '%Y%m').date() # df[0] -> month
        df_subway_traffic_month_hourly = pd.concat([df_subway_traffic_month_hourly, df])
        time.sleep(0.1)
        
        # print(current_date , month_date , deadline)
        if current_date > month_date > deadline:
            ActionChains(driver).move_to_element_with_offset(mouse_tracker, 0, 0).click_and_hold().move_by_offset(0,6).perform()
            driver.implicitly_wait(0.5)
        else:
            break
    

    # 데이터 전처리
    df_subway_traffic_month_hourly.columns = columns_list
    df_subway_traffic_month_hourly.drop_duplicates(keep='first', inplace=True)
    df_subway_traffic_month_hourly.reset_index(drop=True, inplace=True)

    df_subway_traffic_month_hourly.drop('작업일자', axis=1, inplace=True)
    df_subway_traffic_month_hourly.rename(columns={'사용월':'month', '호선명':'line', '지하철역':'station'}, inplace=True)
    df_subway_traffic_month_hourly['month']=pd.to_datetime(df_subway_traffic_month_hourly["month"], format='%Y%m').dt.strftime('%Y-%m-%d %H:%M:%S')
    df_subway_traffic_month_hourly = df_subway_traffic_month_hourly.apply(lambda x: x.astype('int64') if x.dtype == 'float64' else x)

    
    # 3개월 이전을 넘어가는 데이터 삭제
    deadline += relativedelta(months=1)
    df_subway_traffic_month_hourly = df_subway_traffic_month_hourly[df_subway_traffic_month_hourly['month'].between(str(deadline)[:7], df_subway_traffic_month_hourly["month"][0])]

    return df_subway_traffic_month_hourly


def get_driver(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--window-size=1920,1080')
    
    driver = webdriver.Chrome('./chromedriver', options=options)
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

    time.sleep(0.05)


    # 검색명 input tag 입력
    driver.find_element(By.XPATH, '//*[@id="txtFilter"]').send_keys(line_name)
    driver.implicitly_wait(5)
    time.sleep(0.05)

    # 조회 버튼 클릭
    driver.find_element(By.XPATH, '//*[@id="frmSheet"]/div[3]/button[3]').click()
    driver.implicitly_wait(10)
    time.sleep(1.5)

    # 1호선의 경우 '공항철도 1호선' 이 포함되는 것에 대한 예외 if
    if line_name=='1호선':
        # column 클릭마다 정렬 기준 변경 process, recent -> DESC -> ACS 
        line_sort = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_colHead_AX_0_AX_1"]')
        ActionChains(driver).click(line_sort).perform()
        driver.implicitly_wait(5)
        ActionChains(driver).click(line_sort).perform()
        driver.implicitly_wait(5)
        time.sleep(0.2)

    return driver



def run_crawling():
    lines = ['1호선', '2호선', '3호선',' 4호선', '7호선']
    now = datetime.datetime.now().day
    path_subway_traffic_daily = './daily/subway_traffic_daily.json'
    path_subway_traffic_month_hourly = './daily/subway_traffic_month_hourly.json'
    path_station = './daily/station.json'

    df_subway_traffic_daily = pd.DataFrame()
    df_subway_traffic_month_hourly = pd.DataFrame()
    # 파일 존재시 삭제
    if os.path.isfile(path_subway_traffic_daily):
        os.remove('./daily/subway_traffic_daily.json')
    if os.path.isfile(path_subway_traffic_month_hourly):
        os.remove('./daily/subway_traffic_month_hourly.json')
    if os.path.isfile(path_station):
        os.remove('./daily/station.json')

    for line in lines:
        # case 1
        df1 = subway_traffic_daily(line)
        df_subway_traffic_daily = pd.concat([df_subway_traffic_daily, df1])
        time.sleep(0.2)
        # if now == 4: # 매월 4일마다 갱신
        df2 =subway_traffic_month_hourly(line)
        df_subway_traffic_month_hourly = pd.concat([df_subway_traffic_month_hourly, df2])
        time.sleep(0.2)

        # # case 2
        # subway_traffic_daily(line).to_csv('subway_traffic_daily.csv', mode='a', header=not os.path.exists(path_subway_traffic_daily))
        # subway_traffic_month_hourly(line).to_csv('subway_traffic_month_hourly.csv', mode='a', header=not os.path.exists(path_subway_traffic_month_hourly))
    

    df_subway_traffic_daily['date'] = pd.to_datetime(df_subway_traffic_daily['date']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df_stations = df_subway_traffic_daily[['station','line']].drop_duplicates(subset=['station','line'])
    
    
    df_stations.to_json('./daily/station.json',orient='records',force_ascii=False)
    df_subway_traffic_daily.to_json('./daily/subway_traffic_daily.json',orient='records',force_ascii=False)
    df_subway_traffic_month_hourly.to_json('./daily/subway_traffic_month_hourly.json',orient='records',force_ascii=False)
    pass
    # return df_subway_traffic_daily, df_subway_traffic_month_hourly

def main():
    run_crawling()


if __name__ == "__main__":
    main()
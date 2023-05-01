import pandas as pd
import numpy as np
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--window-size=1920,1080')

# 사용 예시.
# from lds_scraper import SubwayInfo
# subway = SubwayInfo()
# subway.daily('1호선')
# subway.hourly('1호선')

class SubwayInfo:
    def daily(self, line_name):
        self.url = "https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do"
        self.line_name = line_name
        driver = self.get_driver()
        self.move_to_data(driver)
        columns = ['date', 'line', 'station', 'in', 'out', 'upload_date']

        # 테이블 스크롤 내리고, 데이터 저장
        mouse_tracker = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')
        res = pd.DataFrame(columns=columns)
        scrollbar = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollTrackY"]')
        scroll_height = scrollbar.size['height']

        # y = 스크롤 핸들의 절댓값 y좌표, -7을 한 이유는 스크롤바 최상단을 클릭하면 다시 위로 가는 에러 발생
        y = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]').size['height'] - 7

        # 스크롤바의 길이가 추후에 변해도 에러 발생 방지
        while y < scroll_height:
            ActionChains(driver).move_to_element_with_offset(mouse_tracker, 0, 0).click_and_hold().move_by_offset(0,6).perform()
            tbody = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_tbody"]')
            tbody_split = np.array(tbody.text.split('\n')).reshape(-1, 6)
            df = pd.DataFrame(tbody_split, columns=columns)
            res = pd.concat([res, df])
            y += 6
            time.sleep(0.3)

        # 데이터 전처리
        res = res.drop_duplicates()
        res = res.apply(lambda x: x.str.replace(',',''))
        res[["in", "out"]] = res[["in", "out"]].apply(pd.to_numeric)
        res[["date", "upload_date"]] = res[["date", "upload_date"]].apply(pd.to_datetime)

        return res
    
    def hourly(self, line_name):
        self.url = "https://data.seoul.go.kr/dataList/OA-12252/S/1/datasetView.do"
        self.line_name = line_name
        driver = self.get_driver()
        self.move_to_data(driver)

        # 데이터 수집
        current_date = pd.Timestamp.now()
        res = pd.DataFrame()
        mouse_tracker = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')

        # if condition: 보고 있는 데이터 프레임의 마지막 월이 현재 월보다 3개월 이상 차이나면 break
        while True:
            ActionChains(driver).move_to_element_with_offset(mouse_tracker, 0, 0).click_and_hold().move_by_offset(0,6).perform()
            html = driver.page_source
            df = pd.read_html(html)[5].iloc[1:-1,:-1]
            date_of_data  = pd.to_datetime(df[0].iloc[-1], format='%Y%m')

            res = pd.concat([res, df])
            if current_date.year*12+current_date.month-(date_of_data.year*12+date_of_data.month) > 3:
                break
            time.sleep(0.2)

        # 데이터 전처리
        res = res.drop_duplicates()
        res = res.apply(lambda x: x.str.replace(',','') if x.dtype == 'str' else x)

        columns = pd.read_html(html)[4]
        columns = columns.squeeze().tolist()
        columns = list(map(lambda x: x.replace('T', ''), columns))
        res.columns = columns

        res["사용월"] = pd.to_datetime(res["사용월"], format='%Y%m')
        res["작업일자"] = pd.to_datetime(res["작업일자"], format='%Y%m%d')
        res = res.apply(lambda x: x.astype(int) if x.dtype == 'float64' else x)

        # 2개월 이내 데이터만 추출
        res = res.loc[res['사용월'] > current_date - pd.DateOffset(months=3)]

    def get_driver(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(self.url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="AXGridTarget_AX_tbody"]')))
        return driver

    def move_to_data(self, driver):
        # 검색 필드 선택
        select_element = driver.find_element(By.NAME, 'filterCol')
        select = Select(select_element)
        select.select_by_value('LINE_NUM')

        # 검색어 입력
        search = driver.find_element(By.NAME, 'txtFilter')
        submit = driver.find_element(By.XPATH, '//*[@id="frmSheet"]/div[3]/button[3]/span')
        ActionChains(driver).send_keys_to_element(search, self.line_name).perform()
        time.sleep(1)
        ActionChains(driver).click(submit).perform()
        time.sleep(1)
        ActionChains(driver).scroll_by_amount(0, 200).perform()
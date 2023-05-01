from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def daily():
    driver.get("https://data.seoul.go.kr/dataList/OA-12914/S/1/datasetView.do")
    driver.implicitly_wait(3)

    button = driver.find_element(By.XPATH, '//*[@id="selt_filterCol"]')
    ActionChains(driver).click(button).perform()
    driver.implicitly_wait(1)

    button.send_keys('호선명')
    button.send_keys(Keys.RETURN)

    key_input = driver.find_element(By.XPATH, '//*[@id="txtFilter"]')
    key_input.send_keys("7호선") 
    driver.implicitly_wait(1)

    search_click = driver.find_element(By.XPATH, '//*[@id="frmSheet"]/div[3]/button[3]/span')
    ActionChains(driver).click(search_click).perform()
    driver.implicitly_wait(1)

    
    data = pd.DataFrame()
    previous_scroll_position = -1
    current_scroll_position = 0

    while True:
        html = driver.page_source
        df = pd.read_html(html)[5].iloc[1:-1, :-1]
        data = pd.concat([data, df], axis=0)
        driver.implicitly_wait(1)

        scroll = driver.find_element(By.XPATH, '//*[@id="AXGridTarget_AX_scrollYHandle"]')
        previous_scroll_position = current_scroll_position
        current_scroll_position = scroll.location['y']

        ActionChains(driver).click_and_hold(scroll).perform()
        ActionChains(driver).move_by_offset(0,5).perform()
        ActionChains(driver).release(scroll).perform()
        driver.implicitly_wait(1)

        if previous_scroll_position == current_scroll_position:
            break


    # 주미님의 전처리를 사용하였습니다.
    data.columns = ['date', 'line', 'station_name', 'people_in', 'people_out', 'upload_date']
    data = data.reset_index(drop=True)  
    driver.implicitly_wait(1)

    d = data
    d['people_in'] = pd.to_numeric(d['people_in'], errors='coerce').fillna(0).astype(int)
    d['people_out'] = pd.to_numeric(d['people_out'], errors='coerce').fillna(0).astype(int)
    d['date'] = pd.to_numeric(d['date'], errors='coerce').fillna(0).astype(int)
    d['date'] = pd.to_datetime(d['date'], format='%Y%m%d', errors='coerce')  # Added errors='coerce'
    d['upload_date'] = pd.to_numeric(d['upload_date'], errors='coerce').fillna(0).astype(int)
    d['upload_date'] = pd.to_datetime(d['upload_date'], format='%Y%m%d', errors='coerce')  # Added errors='coerce'
    return d

daily()
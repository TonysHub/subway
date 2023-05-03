import sqlite3
import pandas as pd

# 시간 측정하기 위해 사용
import time
import datetime




# 받아온 dataframe을 database로 insert 
# start 와 end는 database 에 insert 하는 데에 걸리는 시간을 측정하기 위하여 추가
def insert_subway_traffic(df_subway_traffic_daily,df_subway_traffic_month_hourly,df_stations_line):
    start = time.time()
    
    
    # slug 컬럼 생성 후 line 값 가져와서 보여주기
    
    conn = sqlite3.connect('./db.sqlite3')
    df_subway_traffic_daily.to_sql('TB_TRAFFIC_DAILY', conn, if_exists='replace',index =False)
    df_subway_traffic_month_hourly.to_sql('TB_TRAFFIC_HOURLY', conn, if_exists='replace',index =False)
    df_stations_line.to_sql('TB_STATIONS', conn, if_exists = 'replace', index = False)
    
    
    
    
    end = time.time()
    return print(f' {len(df_stations_line) + len(df_subway_traffic_daily) + len(df_subway_traffic_month_hourly)} row success {str(datetime.timedelta(seconds=end-start)).split(".")[0]}')

    

def main():
    
    df_subway_traffic_daily = pd.read_csv('subway_traffic_daily.csv')
    df_subway_traffic_month_hourly = pd.read_csv('subway_traffic_month_hourly.csv')
    
    df_subway_traffic_month_hourly.rename(columns = {'Unnamed: 0' : 'id'}, inplace = True )
    df_subway_traffic_daily.rename(columns = {'Unnamed: 0' : 'id'}, inplace = True )
    
    
    df_stations_line = df_subway_traffic_daily[['id','station','line']].drop_duplicates()
    df_stations_line['slug'] = df_stations_line['line']
    
    

    
    insert_subway_traffic(df_subway_traffic_daily, df_subway_traffic_month_hourly, df_stations_line)
    
    print('success')

    pass




if __name__ == "__main__":
    main()
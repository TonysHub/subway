import sqlite3
import pandas as pd


# 받아온 dataframe을 database로 insert 
# start 와 end는 database 에 insert 하는 데에 걸리는 시간을 측정하기 위하여 추가
def insert_subway_traffic(df_subway_traffic_daily,df_subway_traffic_month_hourly,df_stations_line):
    # slug 컬럼 생성 후 line 값 가져와서 보여주기
    conn = sqlite3.connect('./db.sqlite3')
    df_subway_traffic_daily.to_sql('TB_TRAFFIC_DAILY', conn, if_exists='replace',index =False)
    df_subway_traffic_month_hourly.to_sql('TB_TRAFFIC_HOURLY', conn, if_exists='replace',index =False)
    df_stations_line.to_sql('TB_STATIONS', conn, if_exists = 'replace', index = False)
    


    

def main():
    # 읽어오고 전처리
    daily = pd.read_csv('subway_traffic_daily.csv')
    hourl = pd.read_csv('subway_traffic_month_hourly.csv')
    daily.rename(columns = {'Unnamed: 0' : 'id'}, inplace = True )
    hourl.rename(columns = {'Unnamed: 0' : 'id'}, inplace = True )
    stations = daily[['id','station','line']].drop_duplicates(subset=['station','line'])
    stations['slug'] = stations['line']
    
    
    # 받아온 dataframe을 database로 insert 
    insert_subway_traffic(daily, hourl, stations)
    
    print('success')

    pass




if __name__ == "__main__":
    main()
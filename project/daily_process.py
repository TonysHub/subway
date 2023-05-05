# 현재 파일 위치
# subway/project/daily_process.py
import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
import django
django.setup()

import json
from django.core.exceptions import ValidationError
from scraper.models import *
from scraper_api.serializers import *
import daily.crawler as crawler
import rest_framework

# daily/crawler.py 파일 실행
def run_crawling() :
    """
    daily/crawler.py 파일 실행
    """
    crawler.run_crawling()



def create_migrations():
    """
    makemigrations 와 migrate 명령어 실행
    """
    os.system("python manage.py makemigrations")
    os.system("python manage.py migrate")



def insert_data_to_database(path, serializers):
    """
    해당 경로(path) 에 있는 json 파일을 읽어 온 후 serializer를 사용하여 데이터베이스에 저장합니다 ( 저장 O, 수정 X )
    데이터베이스에 중복된 데이터가 있는지 ( models에 정의해 놓은 unique_together로 적용 ) 확인 후, 없으면 저장
    """
    f = open(path, encoding="UTF-8")
    dataset = json.loads(f.read())
    
    unique_error_count = 0
    another_error_count = 0
    for data in dataset :
        serializer = serializers(data=data)#,partial=True)
        try  :
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e  :
            # print(e)
            if ("must make a unique set" in str(e)):
                unique_error_count += 1
            else:
                another_error_count +=1
        
    print(f'{serializers} success [{len(dataset)-unique_error_count-another_error_count} / {len(dataset)}]')
    print(f'unique error count : {unique_error_count}, another error count : {another_error_count}')



def run():
    """
    크롤링 진행 후 만들어진 json 파일을 읽어와 serializer 기능을 사용하여 Database에 저장하는 기능을 합니다
    
    1. run_crawling() 
    - daily/crawler.py 파일 실행
    
    2. create_migrations()
    - makemigrations 와 migrate 명령어 실행
    
    3. insert_data_to_database(path, serializers) 
    - 해당 경로에 있는 json 파일을 읽어 온 후 serializer를 사용하여 데이터베이스에 저장합니다 ( 저장 O, 수정 X )
    - 데이터베이스에 중복된 데이터가 있는지 ( models에 정의해 놓은 unique_together로 적용 ) 확인 후, 없으면 저장
    
    
    """
    # run_crawling 주석 시 크롤링 진행하지 않고 데이터 적재만 진행
    # run_crawling()
    
    
    create_migrations()
    
    insert_data_to_database("./daily/subway_traffic_daily.json", DailyTrafficSerializer)
    insert_data_to_database("./daily/subway_traffic_month_hourly.json", HourlyTrafficSerializer)
    insert_data_to_database("./daily/station.json", StationsSerializer)
    
def main():
    run()    
    
if __name__ == "__main__":
    main()




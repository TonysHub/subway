# 현재 파일 위치
# subway/project/daily_process.py
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
import django
django.setup()



import json
from django.core.exceptions import ValidationError
from scraper.models import *
from scraper_api.serializers import *
import daily.crawler as crawler
import rest_framework

def run_crawling() :
    crawler.run_crawling()

def insert_data_to_database(path, serializers):
    f = open(path, encoding="UTF-8")
    dataset = json.loads(f.read())
    
    unique_error_count = 0
    another_error_count = 0
    for data in dataset :
        serializer = serializers(data=data)#,partial=True)

        
        # serializer.is_valid(raise_exception=True)
        
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
    # run_crawling()
    
    insert_data_to_database("./daily/subway_traffic_daily.json", DailyTrafficSerializer)
    insert_data_to_database("./daily/subway_traffic_month_hourly.json", HourlyTrafficSerializer)
    insert_data_to_database("./daily/station.json", StationsSerializer)
    
    
    
def main():
    run()    
    

if __name__ == "__main__":
    main()




import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
import django
django.setup()



import json
from django.core.exceptions import ValidationError
from scraper.models import *
from scraper_api.serializers import *
import daily.crawler as crawler


def run_crawling() :
    crawler.run_crawling()

def insert_data_to_database(path, serializers):
    f = open(path, encoding="UTF-8")
    dataset = json.loads(f.read())
    
    count = 0
    for data in dataset :
        serializer = serializers(data=data)#,partial=True)

        if not serializer.is_valid():
            count += 1
        else :
            serializer.save()
        
    print(f'{serializers} the number of failed data saves   : {count}')

            

def run():
    # run_crawling()
    
    insert_data_to_database("./daily/subway_traffic_daily.json", DailyTrafficSerializer)
    insert_data_to_database("./daily/subway_traffic_month_hourly.json", HourlyTrafficSerializer)
    insert_data_to_database("./daily/station.json", StationsSerializer)
    
    
    
def main():
    run()    
    

if __name__ == "__main__":
    main()




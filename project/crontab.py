from datetime import datetime

def startCrawler():
    print('crontab.py startCrawler', datetime.now())
    return exec(open('daily_process.py').read())

def startTest():
    print('crontab.py startTest', datetime.now())
    return print('Success Test')
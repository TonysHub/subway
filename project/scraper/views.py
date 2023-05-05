from django.shortcuts import render
from django.views.generic import ListView
from django.views import generic
from django.shortcuts import get_object_or_404

from .models import *

# for plotly
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd

class IndexView(ListView):
    template_name = 'scraper/index.html'
    context_object_name = 'all_lines'
    
    def get_queryset(self):
        return Stations.objects.values('line').distinct()



# 추후에 CBV로 변경
def line_details(request, slug):
    obj = Stations.objects.filter(line=slug)
    line_name = slug
    return render(request, 'scraper/line_details.html', {'obj': obj, 'line_name': line_name})


def station_details(request, line, station):

    obj = get_object_or_404(Stations, station=station, line=line)
    
    obj_DailyTraffic = DailyTraffic.objects.filter(station=obj.station, line=obj.line)
    
    obj_HourlyTraffic = HourlyTraffic.objects.filter(station=obj.station, line=obj.line) 

    df_subway_traffic_daily = db_to_df(obj_DailyTraffic)
    df_subway_traffic_month_hourly = db_to_df(obj_HourlyTraffic)

    dailytraffic = dailytraffic_to_plotly(df_subway_traffic_daily, line, station)
    #print(dailytraffic)
    # hourlytraffic = hourlytraffic_to_plotly(df_subway_traffic_month_hourly, line, station)

    return render(request, 'scraper/station_details.html', {'station': obj, 'dailytraffic': dailytraffic})

def search_station(request):
    if request.method == "POST":
        query = request.POST["searched"]
        stations = Stations.objects.filter(station=query)
        return render(request, 'scraper/search_station.html', {'stations': stations, 'station_name': query})
    else:
        return render(request, 'scraper/search_station.html', {})
    
# date, month 데이터 형식 수정
def db_to_df(obj):
    df = pd.DataFrame(obj.values())
    if 'date' in df.columns:
        df['date'] = df['date'].dt.date
    else:
        df['month'] = df['month'].dt.date
    return df

def hourlytraffic_to_plotly(df, line, station):

    
    return df



def dailytraffic_to_plotly(df, line, station):
    information = {}

    for _, row in df.iterrows():
        station = row['station']
        date = row['date']
        people_in = row['people_in']
        people_out = row['people_out']
        if station not in information:
            information[station] = {}

        if date not in information[station]:
            information[station][date] = (people_in, people_out)

        print(information.items())
    
    def find_total_passenger(date_data):
        return sum(people_in + people_out for people_in, people_out in date_data.values())

    station_totals = {station: find_total_passenger(date_data) for station, date_data in information.items()}

    # 어느역을 기준으로 그래프를 그릴지를 나타내는 변수 target_station
    # 역을 클릭하면 해당 역의 이름이 나오면 될 거 같습니다.
    target_station = station

    answer = []

    # 강남역.value = {날짜1:(people_in,people_out), 날짜2: (people_in,people_out)}
    if target_station in information:
        date_data = information[target_station]
        dates = []
        total_passengers = []

        for date, (people_in, people_out) in date_data.items():
            dates.append(date)
            total_passengers.append(people_in + people_out)

            # reversed되어 있던 축을 돌림
        sorted_dates, sorted_total_passengers = zip(*sorted(zip(dates, total_passengers)))

        sorted_dates = pd.to_datetime(sorted_dates)
        dates_with_day = sorted_dates.strftime('%m-%d<br>(%a)') # 월 - 일로 하되 요일은 밑으로 나오게함
        
        trace = go.Scatter(x=dates_with_day, y=sorted_total_passengers, mode='lines+markers', name=target_station, marker=dict(color='red'))
        answer.append(trace)
        print(answer)
    fig = go.Figure(data=answer)
    fig.update_layout(title=f'전체 승객수 in {target_station}역', xaxis_title='Date', yaxis_title='역내 유동인구 수')
    fig.update_xaxes(tickangle=0, tickvals=dates_with_day, tickfont=dict(size=10))
    line_chart = fig.to_html(full_html=False, include_plotlyjs=False)
    print(fig)
    return line_chart
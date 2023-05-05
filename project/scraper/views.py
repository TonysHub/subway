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
    hourlytraffic = hourlytraffic_to_plotly(df_subway_traffic_month_hourly, line, station)

    return render(request, 'scraper/station_details.html', {'station': obj, 'dailytraffic':dailytraffic, 'hourlytraffic': hourlytraffic})


def search_station(request):
    if request.method == "POST":
        query = request.POST["searched"]
        stations = Stations.objects.filter(station=query)
        return render(request, 'scraper/search_station.html', {'stations': stations, 'station_name': query})
    else:
        return render(request, 'scraper/search_station.html', {})


def search_station(request):
    if request.method == "POST":
        query = request.POST["searched"]
        stations = Stations.objects.filter(station=query)
        return render(request, 'scraper/search_station.html', {'stations': stations, 'station_name': query})
    else:
        return render(request, 'scraper/search_station.html', {})


def hourlytraffic_to_plotly(df, line, station):
    # 우리가 보고자 하는 Month, Station을 입력으로 받습니다.
    target_station = station
    month_list = df['month'].unique()
    
    # 보여줄 달과 보여줄 역 선택
    colors = ['red', 'gray', 'steelblue']

    fig = go.Figure()

    for i, target_month in enumerate(month_list):
        # 보여줄 역에 해당하는 데이터프레임을 선택
        filtered_data = df[(df['month']==target_month) & (df['line'] == line)]
        target_month = str(target_month)[:-3]
        
        answer = []
        hourlist = []

        # in_, out_으로 시작하는 부분부터 
        for col in filtered_data.columns[3:]:
            # in이면
            if col.startswith('in_'): 
                in_data = filtered_data.iloc[0][col]
            # out이면 / in-out 번갈아가면서 
            elif col.startswith('out_'):
                out_data = filtered_data.iloc[0][col]
                # 유동인구 고려할때 토탈로
                total = in_data + out_data
                answer.append(total)

                hour = col[4:6]
                hourlist.append(hour)

        color = colors[i]
        trace_total = go.Scatter(x=hourlist, y=answer, mode='lines+markers', name=target_month, marker=dict(color=color))
        fig.add_trace(trace_total)

    fig.update_layout(title=f'Hourly 그래프 for {target_station} Station in 3 months',
                    xaxis_title='시간(Hour)', yaxis_title='역내 유동인구 수',
                    xaxis=dict(tickangle=0), width=900, height=400)

    line_chart = fig.to_html(full_html=False, include_plotlyjs=False)
    return line_chart


def dailytraffic_to_plotly(df, line, station):
    information = {}
    target_station = station
    
    # 데이터프레임을 활용한 딕셔너리 information 생성
    for _, row in df.iterrows():
        station = row['station']
        date = row['date']
        people_in = row['people_in']
        people_out = row['people_out']

        if station not in information:
            information[station] = {}

        if date not in information[station]:
            information[station][date] = (people_in, people_out)

    answer = []

    # 보여줄 역 선택
    if target_station in information:
        date_data = information[target_station]
        dates = []
        total_passengers = []

        # people in과 people out을 합쳐서 사용
        for date, (people_in, people_out) in date_data.items():
            dates.append(date)
            total_passengers.append(people_in + people_out)

        sorted_dates, sorted_total_passengers = zip(*sorted(zip(dates, total_passengers)))

        sorted_dates = pd.to_datetime(sorted_dates)
        dates_with_day = sorted_dates.strftime('%m-%d<br>(%a)') # 월 - 일로 하되 요일은 밑으로 나오게함

        trace = go.Scatter(x=dates_with_day, y=sorted_total_passengers, mode='lines+markers', name=target_station, marker=dict(color='red'))
        answer.append(trace)

    fig = go.Figure(data=answer)
    fig.update_layout(title=f'전체 승객수 in {target_station}역', xaxis_title='Date', yaxis_title='역내 유동인구 수', width=900, height=400)
    fig.update_xaxes(tickangle=0, tickvals=dates_with_day, tickfont=dict(size=10))
    
    line_chart = fig.to_html(full_html=False, include_plotlyjs=False)
    return line_chart


# date, month 데이터 형식 수정
def db_to_df(obj):
    df = pd.DataFrame(obj.values())
    if 'date' in df.columns:
        df['date'] = df['date'].dt.date
    else:
        df['month'] = df['month'].dt.date
    return df
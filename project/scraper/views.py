from django.shortcuts import render
from django.views.generic import ListView
from django.views import generic
from django.shortcuts import get_object_or_404
from .models import *
import datetime

# for plotly
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots


class IndexView(ListView):
    template_name = "scraper/index.html"
    context_object_name = "all_lines"

    def get_queryset(self):
        return Stations.objects.values("line").distinct()


# 추후에 CBV로 변경
def line_details(request, slug):
    obj = Stations.objects.filter(line=slug)
    line_name = slug

    obj_HourlyTraffic = HourlyTraffic.objects.filter(line=line_name)

    df_subway_traffic_month_hourly = db_to_df(obj_HourlyTraffic)
    line_details_plot = line_hourly_traffic_to_plot(
        df_subway_traffic_month_hourly, line_name
    )

    return render(
        request,
        "scraper/line_details.html",
        {"obj": obj, "line_name": line_name, "line_details_plot": line_details_plot},
    )


def station_details(request, line, station):
    obj = get_object_or_404(Stations, station=station, line=line)

    obj_DailyTraffic = DailyTraffic.objects.filter(station=obj.station, line=obj.line)
    obj_HourlyTraffic = HourlyTraffic.objects.filter(station=obj.station, line=obj.line)

    df_subway_traffic_daily = db_to_df(obj_DailyTraffic)
    df_subway_traffic_month_hourly = db_to_df(obj_HourlyTraffic)

    dailytraffic = dailytraffic_to_plotly(df_subway_traffic_daily, line, station)
    hourlytraffic = hourlytraffic_to_plotly(
        df_subway_traffic_month_hourly, line, station
    )

    return render(
        request,
        "scraper/station_details.html",
        {"station": obj, "dailytraffic": dailytraffic, "hourlytraffic": hourlytraffic},
    )


def search_station(request):
    if request.method == "POST":
        query = request.POST["searched"]
        stations = Stations.objects.filter(station=query)
        return render(
            request,
            "scraper/search_station.html",
            {"stations": stations, "station_name": query},
        )
    else:
        return render(request, "scraper/search_station.html", {})


def hourlytraffic_to_plotly(df, line, station):
    # 우리가 보고자 하는 Month, 그리고 우리가 보고자 하는 Station을 입력으로 받습니다.
    target_station = station
    month_list = df["month"].unique()
    colors = ["red", "gray", "steelblue"]

    fig = go.Figure()

    for i, target_month in enumerate(month_list):
        # 보여줄 역에 해당하는 데이터프레임을 선택
        filtered_data = df[(df["month"] == target_month) & (df["line"] == line)]
        target_month = str(target_month)[:-3]

        answer = []
        hourlist = []

        # in_, out_으로 시작하는 column 부분부터
        for col in filtered_data.columns[3:]:
            if col.startswith("in_"):
                in_data = filtered_data.iloc[0][col]
            elif col.startswith("out_"):
                out_data = filtered_data.iloc[0][col]
                # 유동인구 고려할때 토탈로
                total = in_data + out_data
                answer.append(total)

                hour = col[4:6]
                hourlist.append(hour)

        color = colors[i]
        trace_total = go.Scatter(
            x=hourlist,
            y=answer,
            mode="lines+markers",
            name=target_month,
            marker=dict(color=color),
        )
        fig.add_trace(trace_total)

    fig.update_layout(
        title=f"Hourly 그래프 for {target_station} Station in 3 months",
        xaxis_title="시간(Hour)",
        yaxis_title="역내 유동인구 수",
        xaxis=dict(tickangle=0),
        width=900,
        height=400,
    )

    line_chart = fig.to_html(full_html=False, include_plotlyjs=False)
    return line_chart


def dailytraffic_to_plotly(df, line, station):
    information = {}
    target_station = station

    for _, row in df.iterrows():
        station = row["station"]
        date = row["date"]
        people_in = row["people_in"]
        people_out = row["people_out"]

        if station not in information:
            information[station] = {}
        if date not in information[station]:
            information[station][date] = (people_in, people_out)

    # 어느역을 기준으로 그래프를 그릴지를 나타내는 변수 target_station
    # 강남역.value = {날짜1:(people_in,people_out), 날짜2: (people_in,people_out)}
    answer = []
    if target_station in information:
        date_data = information[target_station]
        dates = []
        total_passengers = []

        for date, (people_in, people_out) in date_data.items():
            dates.append(date)
            total_passengers.append(people_in + people_out)

        # reversed되어 있던 축을 돌림
        sorted_dates, sorted_total_passengers = zip(
            *sorted(zip(dates, total_passengers))
        )

        sorted_dates = pd.to_datetime(sorted_dates)
        dates_with_day = sorted_dates.strftime(
            "%m-%d<br>(%a)"
        )  # 월 - 일로 하되 요일은 밑으로 나오게함

        trace = go.Scatter(
            x=dates_with_day,
            y=sorted_total_passengers,
            mode="lines+markers",
            name=target_station,
            marker=dict(color="red"),
        )
        answer.append(trace)

    fig = go.Figure(data=answer)
    fig.update_layout(
        title=f"전체 승객수 in {target_station}역",
        xaxis_title="Date",
        yaxis_title="역내 유동인구 수",
        width=900,
        height=400,
    )
    fig.update_xaxes(tickangle=0, tickvals=dates_with_day, tickfont=dict(size=10))

    line_chart = fig.to_html(full_html=False, include_plotlyjs=False)
    return line_chart


def line_hourly_traffic_to_plot(df, line):
    df["commute_work"] = df.loc[:, "in_0405":"out_0910"].sum(axis=1)
    df["commute_home"] = df.loc[:, "in_1718":"out_2122"].sum(axis=1)
    df["month"] = pd.to_datetime(df["month"])
    today = datetime.datetime.now().strftime("%Y-%m")
    one_month_ago = pd.to_datetime(today) - pd.DateOffset(months=1)
    mask = df["month"] == one_month_ago
    result = df.loc[mask]
    df_filtered = result[(result["line"] == line)]
    fig = make_subplots(rows=2, cols=1, subplot_titles=("출근시간", "퇴근시간"))

    fig.add_trace(
        go.Bar(x=df_filtered["station"], y=df_filtered["commute_work"], name="출근시간"),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(x=df_filtered["station"], y=df_filtered["commute_home"], name="퇴근시간"),
        row=2,
        col=1,
    )

    # Customize the layout
    fig.update_layout(height=1000, width=800, title_text="출근시간과 퇴근시간", showlegend=False)
    line_details_plot = fig.to_html(full_html=False, include_plotlyjs=False)
    return line_details_plot


# date, month 데이터 형식 수정
def db_to_df(obj):
    df = pd.DataFrame(obj.values())
    if "date" in df.columns:
        df["date"] = df["date"].dt.date
    else:
        df["month"] = df["month"].dt.date
    return df

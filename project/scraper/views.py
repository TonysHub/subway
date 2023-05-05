from django.shortcuts import render
from django.views.generic import ListView
from django.views import generic
from django.shortcuts import get_object_or_404
from .models import *


# for plotly
from .plotly import *

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


# date, month 데이터 형식 수정
def db_to_df(obj):
    df = pd.DataFrame(obj.values())
    if "date" in df.columns:
        df["date"] = df["date"].dt.date
    else:
        df["month"] = df["month"].dt.date
    return df

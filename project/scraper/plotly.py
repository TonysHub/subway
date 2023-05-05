import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from plotly.subplots import make_subplots
import datetime

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
    two_month_ago = pd.to_datetime(today) - pd.DateOffset(months=2)
    mask = df["month"] >= two_month_ago
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

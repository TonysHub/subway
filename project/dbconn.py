import sqlite3
import pandas as pd


# 받아온 dataframe을 database로 insert
# start 와 end는 database 에 insert 하는 데에 걸리는 시간을 측정하기 위하여 추가


def insert_subway_traffic(daily, hourly, stations):
    with sqlite3.connect("./db.sqlite3") as conn:
        daily.to_sql(
            "TB_TRAFFIC_DAILY",
            conn,
            if_exists="replace",
            dtype={"id": "INTEGER PRIMARY KEY AUTOINCREMENT"},
        )
        hourly.to_sql(
            "TB_TRAFFIC_HOURLY",
            conn,
            if_exists="replace",
            dtype={"id": "INTEGER PRIMARY KEY AUTOINCREMENT"},
        )
        stations.to_sql(
            "TB_STATIONS",
            conn,
            if_exists="replace",
            dtype={"id": "INTEGER PRIMARY KEY AUTOINCREMENT"},
        )


def main():
    # 읽어오고 전처리

    daily = (
        pd.read_csv("subway_traffic_daily.csv")
        .drop(columns="Unnamed: 0")
        .reset_index()
        .rename(columns={"index": "id"})
    )
    hourly = (
        pd.read_csv("subway_traffic_month_hourly.csv")
        .drop(columns="Unnamed: 0")
        .reset_index()
        .rename(columns={"index": "id"})
    )
    stations = (
        daily[["station", "line"]]
        .drop_duplicates(subset=["station", "line"])
        .reset_index()
        .rename(columns={"index": "id"})
    )

    daily["date"] = pd.to_datetime(daily["date"])
    hourly["month"] = pd.to_datetime(hourly["month"])

    stations["slug"] = stations["line"]

    # 받아온 dataframe을 database로 insert

    insert_subway_traffic(daily, hourly, stations)

    print("success")

    pass


if __name__ == "__main__":
    main()

from django.db import models
from django.utils.text import slugify


"""
모델은 총 3개
Stations       컬럼 수 : 4개     ( sqlite table name = TB_SATIONS )
DailyTraffic   컬럼 수 : 6개     ( sqlite table name = TB_TRAFFIC_DAILY )
HourlyTraffic  컬럼 수 : 52개    ( sqlite table name = TB_TRAFFIC_HOURLY )
"""


"""
아래 Stations, DailyTraffic, HourlyTraffic 에 station과 line이 사용되기 때문에 
abstract를 통하여 상속
"""


class Common(models.Model):
    id = models.AutoField(primary_key=True)

    station = models.CharField(max_length=60, null=False, verbose_name="역명")
    line = models.CharField(max_length=20, null=False, verbose_name="호선명")

    class Meta:
        abstract = True


# database name : TB_STATIONS
class Stations(Common):
    slug = models.SlugField()

    class Meta:
        db_table = "TB_STATIONS"

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.line)
        super().save(*args, **kwargs)


# database name : TB_TRAFFIC_DAILY
class DailyTraffic(Common):
    date = models.DateTimeField(null=False, verbose_name="측정일")
    people_in = models.IntegerField(null=False, verbose_name="승차인원")
    people_out = models.IntegerField(null=False, verbose_name="하차인원")

    class Meta:
        db_table = "TB_TRAFFIC_DAILY"
        verbose_name = "일 별 승하차 인원"


# database name : TB_TRAFFIC_HOURLY
class HourlyTraffic(Common):
    month = models.DateTimeField(null=False, verbose_name="측정월")
    in_0405 = models.IntegerField(null=False, verbose_name="승차인원_04시-05시")
    out_0405 = models.IntegerField(null=False, verbose_name="하차인원_04시-05시")
    in_0506 = models.IntegerField(null=False, verbose_name="승차인원_05시-06시")
    out_0506 = models.IntegerField(null=False, verbose_name="하차인원_05시-06시")
    in_0607 = models.IntegerField(null=False, verbose_name="승차인원_06시-07시")
    out_0607 = models.IntegerField(null=False, verbose_name="하차인원_06시-07시")
    in_0708 = models.IntegerField(null=False, verbose_name="승차인원_07시-08시")
    out_0708 = models.IntegerField(null=False, verbose_name="하차인원_07시-08시")
    in_0809 = models.IntegerField(null=False, verbose_name="승차인원_08시-09시")
    out_0809 = models.IntegerField(null=False, verbose_name="하차인원_08시-09시")
    in_0910 = models.IntegerField(null=False, verbose_name="승차인원_09시_-0시")
    out_0910 = models.IntegerField(null=False, verbose_name="하차인원_09시-10시")
    in_1011 = models.IntegerField(null=False, verbose_name="승차인원_10시-11시")
    out_1011 = models.IntegerField(null=False, verbose_name="하차인원_10시-11시")
    in_1112 = models.IntegerField(null=False, verbose_name="승차인원_11시-12시")
    out_1112 = models.IntegerField(null=False, verbose_name="하차인원_11시-12시")
    in_1213 = models.IntegerField(null=False, verbose_name="승차인원_12시-13시")
    out_1213 = models.IntegerField(null=False, verbose_name="하차인원_12시-13시")
    in_1314 = models.IntegerField(null=False, verbose_name="승차인원_13시-14시")
    out_1314 = models.IntegerField(null=False, verbose_name="하차인원_13시-14시")
    in_1415 = models.IntegerField(null=False, verbose_name="승차인원_14시-15시")
    out_1415 = models.IntegerField(null=False, verbose_name="하차인원_14시-15시")
    in_1516 = models.IntegerField(null=False, verbose_name="승차인원_15시-16시")
    out_1516 = models.IntegerField(null=False, verbose_name="하차인원_15시-16시")
    in_1617 = models.IntegerField(null=False, verbose_name="승차인원_16시-17시")
    out_1617 = models.IntegerField(null=False, verbose_name="하차인원_16시-17시")
    in_1718 = models.IntegerField(null=False, verbose_name="승차인원_17시-18시")
    out_1718 = models.IntegerField(null=False, verbose_name="하차인원_17시-18시")
    in_1819 = models.IntegerField(null=False, verbose_name="승차인원_18시-19시")
    out_1819 = models.IntegerField(null=False, verbose_name="하차인원_18시-19시")
    in_1920 = models.IntegerField(null=False, verbose_name="승차인원_19시-20시")
    out_1920 = models.IntegerField(null=False, verbose_name="하차인원_19시-20시")
    in_2021 = models.IntegerField(null=False, verbose_name="승차인원_20시-21시")
    out_2021 = models.IntegerField(null=False, verbose_name="하차인원_20시-21시")
    in_2122 = models.IntegerField(null=False, verbose_name="승차인원_21시-22시")
    out_2122 = models.IntegerField(null=False, verbose_name="하차인원_21시-22시")
    in_2223 = models.IntegerField(null=False, verbose_name="승차인원_22시-23시")
    out_2223 = models.IntegerField(null=False, verbose_name="하차인원_22시-23시")
    in_2324 = models.IntegerField(null=False, verbose_name="승차인원_23시-24시")
    out_2324 = models.IntegerField(null=False, verbose_name="하차인원_23시-24시")
    in_0001 = models.IntegerField(null=False, verbose_name="승차인원_00시-01시")
    out_0001 = models.IntegerField(null=False, verbose_name="하차인원_00시-01시")
    in_0102 = models.IntegerField(null=False, verbose_name="승차인원_01시-02시")
    out_0102 = models.IntegerField(null=False, verbose_name="하차인원_01시-02시")
    in_0203 = models.IntegerField(null=False, verbose_name="승차인원_02시-03시")
    out_0203 = models.IntegerField(null=False, verbose_name="하차인원_02시-03시")
    in_0304 = models.IntegerField(null=False, verbose_name="승차인원_03시-04시")
    out_0304 = models.IntegerField(null=False, verbose_name="하차인원_03시-04시")

    class Meta:
        db_table = "TB_TRAFFIC_HOURLY"
        verbose_name = "시간 별 승하차 인원(월단위)"

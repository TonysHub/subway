from django.db import models

# Create your models here.



# 나중에 Stations.station은 FK 로 변경
class Stations (models.Model):
    station = models.CharField(max_length = 60, primary_key= True)
    line = models.CharField(max_length = 40)
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from scraper.models import *



class CommonSerializer(serializers.Serializer):
    class Meta :
        model = Common
        fields =  '__all__'
        abstract = True
    
class StationsSerializer(CommonSerializer):
    # id = serializers.UUIDField()
    station = serializers.CharField()
    line = serializers.CharField()
    
    class Meta :
        model = Stations
        fields = '__all__'
        fields =  ['station','line']
        validators = [
            UniqueTogetherValidator(
                queryset=Stations.objects.all(),
                fields=['station', 'line']
            )
        ]
    
    
    
    def create(self, validated_data):
        return Stations.objects.create(**validated_data)
        
    
class DailyTrafficSerializer(CommonSerializer):
    station = serializers.CharField()
    line = serializers.CharField()
    people_in = serializers.IntegerField()
    people_out = serializers.IntegerField()
    date = serializers.DateTimeField()
    
    
    class Meta :
        model = DailyTraffic
        fields =  ['station','line','date','people_in','people_out']
        validators = [
            UniqueTogetherValidator(
                queryset=DailyTraffic.objects.all(),
                fields=['station','line','date']
            )
        ]
    
    def create(self, validated_data):
        return DailyTraffic.objects.create(**validated_data)

class HourlyTrafficSerializer(CommonSerializer):
    station = serializers.CharField()
    line = serializers.CharField()
    month = serializers.DateTimeField()
    in_0405 = serializers.IntegerField()
    out_0405 =serializers.IntegerField()
    in_0506 = serializers.IntegerField()
    out_0506 =serializers.IntegerField()
    in_0607 = serializers.IntegerField()
    out_0607 =serializers.IntegerField()
    in_0708 = serializers.IntegerField()
    out_0708 =serializers.IntegerField()
    in_0809 = serializers.IntegerField()
    out_0809 =serializers.IntegerField()
    in_0910 = serializers.IntegerField()
    out_0910 =serializers.IntegerField()
    in_1011 = serializers.IntegerField()
    out_1011 =serializers.IntegerField()
    in_1112 = serializers.IntegerField()
    out_1112 =serializers.IntegerField()
    in_1213 = serializers.IntegerField()
    out_1213 =serializers.IntegerField()
    in_1314 = serializers.IntegerField()
    out_1314 =serializers.IntegerField()
    in_1415 = serializers.IntegerField()
    out_1415 =serializers.IntegerField()
    in_1516 = serializers.IntegerField()
    out_1516 =serializers.IntegerField()
    in_1617 = serializers.IntegerField()
    out_1617 =serializers.IntegerField()
    in_1718 = serializers.IntegerField()
    out_1718 =serializers.IntegerField()
    in_1819 = serializers.IntegerField()
    out_1819 =serializers.IntegerField()
    in_1920 = serializers.IntegerField()
    out_1920 =serializers.IntegerField()
    in_2021 = serializers.IntegerField()
    out_2021 =serializers.IntegerField()
    in_2122 = serializers.IntegerField()
    out_2122 =serializers.IntegerField()
    in_2223 = serializers.IntegerField()
    out_2223 =serializers.IntegerField()
    in_2324 = serializers.IntegerField()
    out_2324 =serializers.IntegerField()
    in_0001 = serializers.IntegerField()
    out_0001 =serializers.IntegerField()
    in_0102 = serializers.IntegerField()
    out_0102 =serializers.IntegerField()
    in_0203 = serializers.IntegerField()
    out_0203 =serializers.IntegerField()
    in_0304 = serializers.IntegerField()
    out_0304 =serializers.IntegerField()

    class Meta :
        model = HourlyTraffic
        fields =  ['station','line','month''in_0405','out_0405','in_0506','out_0506','in_0607','out_0607','in_0708','out_0708','in_0809','out_0809','in_0910','out_0910','in_1011','out_1011','in_1112','out_1112','in_1213','out_1213','in_1314','out_1314','in_1415','out_1415','in_1516','out_1516','in_1617','out_1617','in_1718','out_1718','in_1819','out_1819','in_1920','out_1920','in_2021','out_2021','in_2122','out_2122','in_2223','out_2223','in_2324','out_2324','in_0001','out_0001','in_0102','out_0102','in_0203','out_0203','in_0304','out_0304']     
        validators = [
            UniqueTogetherValidator(
                queryset=HourlyTraffic.objects.all(),
                fields=['station','line','month']
            )
        ]
    
    def create(self, validated_data):
        return HourlyTraffic.objects.create(**validated_data)


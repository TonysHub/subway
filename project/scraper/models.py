from django.db import models
from django.utils.text import slugify
# Create your models here.

# 나중에 Stations.station은 FK 로 변경
class Stations (models.Model):
    station = models.CharField(max_length = 60, primary_key= True)
    line = models.CharField(max_length = 40)
    slug = models.SlugField(max_length = 60, default= '7호선')

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.line)
        super().save(*args, **kwargs)
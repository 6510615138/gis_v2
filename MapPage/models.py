from django.db import models

# Create your models here.
class Province(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=64)

class District(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    province_code = models.PositiveSmallIntegerField()

class Subdistrict(models.Model):
    code = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    district_code = models.PositiveSmallIntegerField()
    is_island = models.BooleanField()
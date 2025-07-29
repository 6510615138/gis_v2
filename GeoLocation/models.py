from django.db import models

class Province(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'province'

class District(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.TextField()
    province_code = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'district'

class Subdistrict(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.TextField()
    district_code = models.IntegerField()
    is_island = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subdistrict'
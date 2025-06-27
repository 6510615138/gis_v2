# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class District(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.TextField()
    province_code = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'district'


class Factory(models.Model):
    name = models.TextField(blank=True, null=True)
    registration_num = models.TextField(primary_key=True)
    type = models.TextField(blank=True, null=True)
    standard = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    subdistrict = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    factory_phone_number = models.TextField(blank=True, null=True)
    owner_name = models.TextField(blank=True, null=True)
    owner_address = models.TextField(blank=True, null=True)
    owner_phone_number = models.TextField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    hp = models.FloatField(blank=True, null=True)
    capital = models.FloatField(blank=True, null=True)
    worker = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factory'


class FactoryTemp(models.Model):
    name = models.TextField(blank=True, null=True)
    registration_num = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    standard = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    subdistrict = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    factory_phone_number = models.TextField(blank=True, null=True)
    owner_name = models.TextField(blank=True, null=True)
    owner_address = models.TextField(blank=True, null=True)
    owner_phone_number = models.TextField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    hp = models.FloatField(blank=True, null=True)
    capital = models.FloatField(blank=True, null=True)
    worker = models.FloatField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factory_temp'


class FactoryTemp1(models.Model):
    name = models.TextField(blank=True, null=True)
    registration_num = models.TextField(blank=True, null=True)
    type = models.FloatField(blank=True, null=True)
    standard = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    subdistrict = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    factory_phone_number = models.TextField(blank=True, null=True)
    owner_name = models.TextField(blank=True, null=True)
    owner_address = models.TextField(blank=True, null=True)
    owner_phone_number = models.TextField(blank=True, null=True)
    purpose = models.TextField(blank=True, null=True)
    hp = models.FloatField(db_column='HP', blank=True, null=True)  # Field name made lowercase.
    capital = models.FloatField(blank=True, null=True)
    worker = models.IntegerField(blank=True, null=True)
    lat = models.IntegerField(blank=True, null=True)
    lng = models.IntegerField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'factory_temp (1)'


class Province(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'province'


class Subdistrict(models.Model):
    code = models.AutoField(primary_key=True)
    name = models.TextField()
    district_code = models.IntegerField()
    is_island = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subdistrict'

from django.db import models

class FactoryCoordinates(models.Model):
    registration_num = models.TextField(primary_key=True)
    name = models.TextField(blank=True, null=True)
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
    worker = models.IntegerField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    status = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'factory_coordinates2'


class FactoryType(models.Model):
    code = models.TextField(primary_key=True)
    num = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    class1 = models.TextField(blank=True, null=True)
    class2 = models.TextField(blank=True, null=True)
    class3 = models.TextField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'factory_type'
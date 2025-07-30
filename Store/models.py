from django.db import models

class Store(models.Model):
    id = models.IntegerField(primary_key=True)
    branch_name = models.TextField(blank=True, null=True)
    store_id = models.IntegerField(blank=True, null=True)
    branch_type = models.TextField(blank=True, null=True)
    format = models.TextField(blank=True, null=True)
    owner = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    province = models.TextField(blank=True, null=True)
    district = models.TextField(blank=True, null=True)
    subdistrict = models.TextField(blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_store3'

from django.db import models


class Region(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'regions'


class Area(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'areas'


class Branch(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    shop_name = models.CharField(max_length=20)
    tel = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    shop_number = models.IntegerField()
    business_time = models.CharField(max_length=50)
    interior = models.CharField(max_length=400, null=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=5)
    longitude = models.DecimalField(max_digits=7, decimal_places=4)
    regist_date = models.DateTimeField(auto_now_add=True)
    notice = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = 'branches'


class Service(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'services'


class BranchService(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'branch_services'

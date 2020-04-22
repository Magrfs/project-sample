from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    birth_date = models.DateTimeField()
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50, unique=True)
    zipcode = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    address_detail = models.CharField(max_length=50)

    class Meta:
        db_table = 'users'

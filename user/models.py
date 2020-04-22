from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=45)
    password = models.CharField(max_length=45)
    name = models.CharField(max_length=45)
    birth_date = models.CharField(max_length=45)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=100, unique=True)
    zipcode = models.CharField(max_length=45)
    address = models.CharField(max_length=100)
    address_detail = models.CharField(max_length=100)
    my_card = models.ForeignKey(
        "UsersInfo", on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'users'

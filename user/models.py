from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=50)
    password = models.CharField(max_length=200)
    name = models.CharField(max_length=50)
    birth_date = models.DateTimeField()
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50, unique=True)
    zipcode = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    address_detail = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'users'

class ClausesConfirmation(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    clausers_id = models.ForeignKey('ClausesOption', on_delete=models.SET_NULL, null=True)
    confirm = models.BooleanField()

    class Meta:
        db_table = 'clauses_confirmations'

class ClausesOption(models.Model):
    type = models.IntegerField()
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=3000)

    class Meta:
        db_table = 'clauses_options'

class ClausesEssentials(models.Model):
    type = models.IntegerField()
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=3000)

    class Meta:
        db_table = 'clauses_essentials'

class UserInfo(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    rank_id = models.ForeignKey('Rank', on_delete=models.SET_NULL, null=True)
    savings_point = models.IntegerField()

    class Meta:
        db_table = 'user_infos'

class Rank(models.Model):
    name = models.CharField(max_length=10)
    image = models.URLField(max_length=1000)

    class Meta:
        db_table = 'ranks'

class Card(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=45)

    class Meta:
        db_table = 'cards'

class Crown(models.Model):
    user_info_id = models.ForeignKey('UserInfo', on_delete=models.SET_NULL, null=True)
    saving_date = models.DateTimeField()
    saving_target = models.CharField(max_length=50)
    saving_crown = models.IntegerField()
    expire_date = models.DateTimeField()

    class Meta:
        db_table = 'user_crowns'

class Coupon(models.Model):
    user_info_id = models.ForeignKey('UserInfo', on_delete=models.SET_NULL, null=True)
    code = models.IntegerField()
    name = models.CharField(max_length=50)
    expire_date = models.DateTimeField()
    is_available = models.BooleanField()

    class Meta:
        db_table = 'user_coupons'

class Inquery(models.Model):
    title = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    answer = models.CharField(max_length=45)

    class Meta:
        db_table = 'inquires'
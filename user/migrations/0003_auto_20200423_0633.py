# Generated by Django 3.0.5 on 2020-04-23 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200423_0542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='address_detail',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

# Generated by Django 3.0.5 on 2020-04-24 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClausesEssentials',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=3000)),
            ],
            options={
                'db_table': 'clauses_essentials',
            },
        ),
        migrations.CreateModel(
            name='ClausesOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=3000)),
            ],
            options={
                'db_table': 'clauses_options',
            },
        ),
        migrations.CreateModel(
            name='Inquery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=45)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'inquires',
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('image', models.URLField(max_length=1000)),
            ],
            options={
                'db_table': 'ranks',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=50)),
                ('birth_date', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('zipcode', models.CharField(max_length=20, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
                ('address_detail', models.CharField(max_length=50, null=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('savings_point', models.IntegerField()),
                ('rank', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.Rank')),
                ('user_relation', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User')),
            ],
            options={
                'db_table': 'user_infos',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='user_info',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.UserInfo'),
        ),
        migrations.CreateModel(
            name='Crown',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saving_date', models.DateTimeField()),
                ('saving_target', models.CharField(max_length=50)),
                ('saving_crown', models.IntegerField()),
                ('expire_date', models.DateTimeField()),
                ('user_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.UserInfo')),
            ],
            options={
                'db_table': 'user_crowns',
            },
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=300)),
                ('name', models.CharField(max_length=50)),
                ('expire_date', models.DateTimeField()),
                ('is_available', models.BooleanField()),
                ('user_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.UserInfo')),
            ],
            options={
                'db_table': 'user_coupons',
            },
        ),
        migrations.CreateModel(
            name='ClausesConfirmation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirm', models.BooleanField()),
                ('clausers', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.ClausesOption')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User')),
            ],
            options={
                'db_table': 'clauses_confirmations',
            },
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=45)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.User')),
            ],
            options={
                'db_table': 'cards',
            },
        ),
    ]

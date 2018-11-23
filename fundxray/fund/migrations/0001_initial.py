# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-06-09 03:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DevInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('record_time', models.DateField()),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FundDeal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('date', models.DateField()),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='FundInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('code', models.CharField(max_length=32)),
                ('company', models.CharField(max_length=64)),
                ('type1', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='FundManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('link', models.CharField(max_length=512)),
                ('desc', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='FundToManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('desc', models.CharField(max_length=512)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fund.FundManager')),
            ],
        ),
        migrations.CreateModel(
            name='FundValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('jjjz', models.FloatField()),
                ('ljjz', models.FloatField()),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='FundValueCalc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32)),
                ('date', models.DateField()),
                ('increases', models.FloatField()),
                ('jitter', models.FloatField()),
                ('type', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='FundValueDeal1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateField()),
                ('month_income', models.FloatField()),
                ('fund', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='fund.FundInfo')),
            ],
        ),
    ]

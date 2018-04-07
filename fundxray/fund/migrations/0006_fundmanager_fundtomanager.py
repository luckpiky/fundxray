# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-02-24 12:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fund', '0005_funddeal'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('desc', models.CharField(max_length=512)),
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
    ]

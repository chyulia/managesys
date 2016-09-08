# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-31 07:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_import', '0024_sales_displistno_sales_millsheetno'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sales_millsheetno',
            name='customerNameEn',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sales_millsheetno',
            name='memoA',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='sales_millsheetno',
            name='memoB',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='sales_millsheetno',
            name='memoC',
            field=models.CharField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='sales_millsheetno',
            name='memoD',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='sales_millsheetno',
            name='mscIndexNo',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='sales_millsheetno',
            name='productNameEn',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='sales_millsheetno',
            name='techTerms',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='sales_millsheetno',
            name='title',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]

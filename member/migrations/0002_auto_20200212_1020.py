# -*- coding: utf-8 -*-z
# Generated by Django 2.0.13 on 2020-02-12 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_pw',
            field=models.CharField(max_length=20),
        ),
    ]

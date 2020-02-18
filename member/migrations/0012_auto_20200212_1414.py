# -*- coding: utf-8 -*-z
# Generated by Django 2.0.13 on 2020-02-12 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0011_auto_20200212_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='member_rank',
            field=models.CharField(choices=[('이사/임원', ((('대표이사',), '대표이사'), (('상무',), '상무'), (('이사',), '이사'))), ('직원', ((('부장',), '부장'), (('차장',), '차장'), (('과장',), '과장'), (('대리',), '대리'), (('주임',), '주임'), ('사원', '사원')))], default='대리', max_length=20),
        ),
    ]

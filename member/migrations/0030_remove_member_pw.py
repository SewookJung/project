# Generated by Django 2.0.13 on 2020-06-15 07:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0029_auto_20200311_1500'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='pw',
        ),
    ]
# Generated by Django 2.0.13 on 2020-02-27 00:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0009_auto_20200221_1412'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assetrent',
            old_name='member_id',
            new_name='member_name',
        ),
    ]
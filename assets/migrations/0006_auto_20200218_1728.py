# Generated by Django 2.0.13 on 2020-02-18 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0005_assetrent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='member_name',
            new_name='member_id',
        ),
    ]

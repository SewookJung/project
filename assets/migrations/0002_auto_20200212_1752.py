# Generated by Django 2.0.13 on 2020-02-12 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='member_id',
            new_name='member_name',
        ),
    ]

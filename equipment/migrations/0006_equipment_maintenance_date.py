# Generated by Django 2.0.13 on 2020-08-18 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0005_auto_20200814_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipment',
            name='maintenance_date',
            field=models.DateField(blank=True, max_length=20, null=True),
        ),
    ]
# Generated by Django 2.0.13 on 2020-02-20 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0006_auto_20200218_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='serial',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='asset',
            name='member_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='member.Member'),
        ),
    ]
# Generated by Django 2.0.13 on 2020-10-22 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0030_remove_member_pw'),
        ('project', '0002_auto_20201022_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='member.Member'),
        ),
    ]

# Generated by Django 2.0.13 on 2020-11-02 06:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0030_remove_member_pw'),
        ('document', '0015_documentbasicform_attach'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentbasicform',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='member.Member'),
        ),
    ]

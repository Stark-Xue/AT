# Generated by Django 3.0.4 on 2020-10-23 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0008_competition_com_log'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='competition',
            name='com_log',
        ),
    ]

# Generated by Django 3.0.4 on 2020-10-18 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deal',
            field=models.BooleanField(default=False),
        ),
    ]

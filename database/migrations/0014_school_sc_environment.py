# Generated by Django 3.0.4 on 2020-10-29 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0013_school'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='sc_environment',
            field=models.TextField(default='ds', verbose_name='校区环境'),
            preserve_default=False,
        ),
    ]
# Generated by Django 3.0.4 on 2020-10-28 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20201023_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='cour_img',
            field=models.ImageField(null=True, upload_to='', verbose_name='竞赛照片'),
        ),
    ]

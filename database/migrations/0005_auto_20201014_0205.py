# Generated by Django 3.0.4 on 2020-10-14 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_auto_20201004_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='com_img',
            field=models.ImageField(default='/static/images/34FBD611-9267-4C81-A38C-4AC2EAD44980.png', upload_to='', verbose_name='公司照片'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='com_log',
            field=models.ImageField(default='/static/images/34FBD611-9267-4C81-A38C-4AC2EAD44980.png', upload_to='', verbose_name='公司log'),
            preserve_default=False,
        ),
    ]

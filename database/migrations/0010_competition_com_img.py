# Generated by Django 3.0.4 on 2020-10-23 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0009_remove_competition_com_log'),
    ]

    operations = [
        migrations.AddField(
            model_name='competition',
            name='com_img',
            field=models.ImageField(default='/static/images/we_Chat.jpg', upload_to='', verbose_name='竞赛照片'),
            preserve_default=False,
        ),
    ]

from django.db import models

# Create your models here.

class Order(models.Model):
    """
    体验课预约表
    """
    telephone = models.CharField(max_length=32, unique=True)
    stu_name = models.CharField(max_length=32, null=True)
    stu_age = models.CharField(max_length=32)
    weChat = models.CharField(max_length=64, null=True)
    deal = models.BooleanField(default=False)


class User(models.Model):
    """
    管理者信息表
    """
    username = models.CharField(verbose_name="用户名", max_length=32, unique=True)
    password = models.CharField(verbose_name="密码", max_length=64)


class Company(models.Model):
    """
    公司信息表
    """
    com_name = models.CharField(max_length=64)
    com_tel = models.CharField(max_length=32)
    com_weChat = models.ImageField(verbose_name='官方微信')
    com_log = models.ImageField(verbose_name='公司log')
    com_img = models.ImageField(verbose_name='公司照片')
    com_validity = models.CharField(max_length=256)
    com_introduction = models.TextField(verbose_name='公司详情',)
    teach_idea = models.TextField(verbose_name='教学理念',)
    school_address = models.TextField(verbose_name='校区分布',)
    recruit = models.TextField(verbose_name='招聘信息',)


class Course(models.Model):
    """
    课程信息表
    """
    cour_name = models.CharField(max_length=32, unique=True)
    cour_validity = models.CharField(max_length=256)
    cour_introduction = models.TextField(verbose_name='课程介绍',)
    cour_img = models.ImageField(verbose_name='竞赛照片', null=True)


class Competition(models.Model):
    """
    竞赛信息表
    """
    com_name = models.CharField(max_length=32, unique=True)
    com_validity = models.CharField(max_length=256)

    com_introduction = models.TextField(verbose_name='竞赛介绍', )
    com_img = models.ImageField(verbose_name='竞赛照片', null=True)
    #com_result = models.ImageField(verbose_name='竞赛成绩', null=True)


class CompetitionResult(models.Model):
    """
    竞赛成绩表
    """
    cr_name = models.CharField(max_length=64, unique=True)
    cr_img = models.ImageField(verbose_name='竞赛照片', null=True)


class School(models.Model):
    """
    校区分布表
    """
    sc_name = models.CharField(max_length=32)
    sc_addr = models.CharField(max_length=256)
    sc_tel = models.CharField(max_length=32)
    sc_environment = models.TextField(verbose_name='校区环境', )
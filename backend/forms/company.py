from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

from database import models

class CompanyForm(django_forms.Form):
    com_name = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '公司名称'}),
    )

    com_tel = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '公司电话'}),
    )

    com_weChat = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '官方微信'}),
    )

    com_validity = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '公司简介', 'rows': '3'})
    )

    com_introduction = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content', 'placeholder': '公司详情'})
    )

    teach_idea = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content', 'placeholder': '教学理念'})
    )

    school_address = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content', 'placeholder': '校区分布'})
    )

    recruit = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content', 'placeholder': '招聘信息'})
    )
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

from database import models

class SchoolForm(django_forms.Form):
    sc_name = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '校区名称'}),
    )

    sc_addr = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '校区详细地址'})
    )

    sc_tel = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '校区联系电话'})
    )

    sc_environment = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content', 'placeholder': '课程详情'})
    )
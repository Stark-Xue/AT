from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

from database import models

class CourseForm(django_forms.Form):
    cour_name = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '课程名称'}),
    )

    cour_validity = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '课程简介', 'rows': '3'})
    )

    cour_introduction = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content', 'placeholder': '课程详情'})
    )
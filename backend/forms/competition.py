from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

from database import models

class CompetitionForm(django_forms.Form):
    com_name = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '竞赛项目名称', 'onchange': 'dianji();' }),
    )

    com_validity = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'form-control', 'placeholder': '竞赛项目简介', 'rows': '3'})
    )

    com_introduction = django_fields.CharField(
        widget=django_widgets.Textarea(attrs={'class': 'kind-content', 'placeholder': '竞赛项目详情'})
    )
from django import forms as django_forms
from django.forms import fields as django_fields
from django.forms import widgets as django_widgets

from database import models

class CompetitionResultForm(django_forms.Form):
    cr_name = django_fields.CharField(
        widget=django_widgets.TextInput(attrs={'class': 'form-control', 'placeholder': '竞赛成绩名称', 'onchange': 'dianji();' }),
    )
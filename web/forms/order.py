from django import forms
from django.forms import fields
from django.forms import widgets

class OrderForm(forms.Form):
    telephone = fields.CharField(
        min_length=11,
        error_messages={
            "min_length": "请输入11位手机号码",
            "required": "手机号不能为空",
        },
        widget=widgets.TextInput(
            attrs={
                "placeholder": "请输入您的手机号码",
                "style": "width:400px; display: inline-block; ",
                "class": "form-control"
            }
        ),
    )
    # stu_name = fields.CharField(
    #
    #     widget=widgets.TextInput(
    #         attrs={
    #             "placeholder": "请输入学生姓名（选填）",
    #             "style": "width:400px; display: inline-block; ",
    #             "class": "form-control"
    #         }
    #     ),
    # )
    stu_age = fields.CharField(
        min_length=1,
        max_length=2,
        error_messages={
            "min_length": "请输入正确的年龄",
            "max_length": "请输入正确的年龄",
            "required": "年龄不能为空",
        },
        widget=widgets.TextInput(
            attrs={
                "placeholder": "请输入学生年龄",
                "style": "width:400px;display: inline-block; ",
                "class": "form-control"
            }
        ),
    )
    # weChat = fields.CharField(
    #     widget=widgets.TextInput(
    #         attrs={
    #             "placeholder": "请输入您的微信号（选填）",
    #             "style": "width:400px;display: inline-block; ",
    #             "class": "form-control"
    #         }
    #     ),
    # )
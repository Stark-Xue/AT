"""AT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from backend import views

urlpatterns = [
    # path('admin/', admin.site.urls),

    path("index/", views.index),
    path("companyIntroduce/", views.companyIntroduce),
    path("upload_img/", views.upload_img),
    path("upload_lbt/", views.upload_lbt),
    path("recruit/", views.recruit),
    path("teach/", views.teach),
    #path("school/", views.school),
    path("baseinfo/", views.baseinfo),
    path("baseinfo_update/", views.baseinfo_update),
    path("upload_avatar/", views.upload_avatar),
    path("upload_log/", views.upload_log),
    path("upload_companyImg/", views.upload_companyImg),

    re_path("competition/edit-(?P<cid>\d+)/", views.competition_edit),
    re_path("competition/read-(?P<cid>\d+)/", views.competition_read),
    path("competition/", views.competition),
    path("competition/add/", views.competition_add),
    re_path("competition/delete/", views.competition_delete),
    path("upload_competition_img/", views.upload_competition_img),

    path("competitionResult/", views.competitionResult),
    path("competitionResult/add/", views.competitionResult_add),
    path("upload_result_img/", views.upload_result_img),
    re_path("competitionResult/read-(?P<cid>\d+)/", views.competitionResult_read),
    re_path("competitionResult/edit-(?P<cid>\d+)/", views.competitionResult_edit),
    re_path("competitionResult/delete/", views.competitionResult_delete),

    path("course/", views.course),
    re_path("course/read-(?P<cid>\d+)/", views.course_read),
    re_path("course/edit-(?P<cid>\d+)/", views.course_edit),
    re_path("course/delete/", views.course_delete),
    path("course/add/", views.course_add),
    path("upload_course_img/", views.upload_course_img),

    path("school/", views.school),
    path("school/add/", views.school_add),
    re_path("school/read-(?P<sid>\d+)/", views.school_read),
    re_path("school/edit-(?P<sid>\d+)/", views.school_edit),
    re_path("school/delete/", views.school_delete),

    path("home/", views.home),
    path("delete_lbt/", views.delete_lbt),

    path("user/", views.user),
    re_path("user/read-(?P<uid>\d+)", views.user_read),
    path("user_update/", views.user_update),
    re_path("user/edit-(?P<uid>\d+)/", views.user_edit),
    path("user/delete/", views.user_delete),
    path("user/add/", views.user_add),
    # path("logout/", views.logout),

    path("order/", views.order),
    re_path("order/deal-(?P<oid>\d+)", views.order_deal),

    path("logout/", views.logout),
]

from django.shortcuts import render, HttpResponse, redirect

from database import models

from .forms.company import CompanyForm
from .forms.competition import CompetitionForm
from .forms.course import CourseForm
from .forms.user import UserForm
from .forms.school import SchoolForm
from .forms.competitionResult import CompetitionResultForm
from AT.settings import base
from utils.pagination import Page

'''
xframe_options_exempt: 页面地址允许frame加载
xframe_options_sameorigin: 页面地址只能被同源域名页面嵌入到frame中
xframe_options_deny: 页面地址不能被嵌入到任何frame中
'''
from django.views.decorators.clickjacking import xframe_options_exempt, xframe_options_sameorigin, xframe_options_deny

import json, os, re

from django.db import transaction

from .auth.auth import check_login

# Create your views here.


@check_login
def order(request):
    data_count = models.Order.objects.filter().all().count()
    undeal_count = models.Order.objects.filter(deal=False).count()
    # print("order", order_obj)
    # for i in order_obj:
    #     print(i.deal, type(i.deal))
    page_obj = Page(request.GET.get("p", 1), data_count, 10, 5)
    page_str = page_obj.page_str("/backend/order/")
    order_obj = models.Order.objects.filter().order_by("deal").all()[page_obj.start: page_obj.end]
    return render(request, "backend_order.html", {
            "order_obj": order_obj,
            "data_count": data_count,
            "undeal_count": undeal_count,
            "page_str": page_str,
        }
    )


@check_login
def order_deal(request, oid):
    models.Order.objects.filter(id=oid).update(deal=True)
    request.session["order_count"] = request.session["order_count"] - 1
    return redirect("/backend/order/")


@check_login
def user(request):
    user_obj = models.User.objects.filter(username=request.session.get("username")).first()
    # users_obj = models.User.objects.filter().all()
    data_count = models.User.objects.filter().all().count()-1
    init_dic = {
        'username': user_obj.username,
        'password': user_obj.password,
    }
    form = UserForm(data=init_dic)
    page_obj = Page(request.GET.get("p", 1), data_count, 10, 5)
    page_str = page_obj.page_str("/backend/user/")
    users_obj = models.User.objects.exclude(username=request.session.get("username")).all()[page_obj.start: page_obj.end]
    return render(request, "backend_user.html", {
            "form": form,
            "user_obj": user_obj,
            "users_obj": users_obj,
            "data_count": data_count,
            "page_str": page_str,
        }
    )


@check_login
def user_read(request, uid):
    if request.method == "GET":
        user_obj = models.User.objects.filter(id=uid).first()
        init_dic = {
            'username': user_obj.username,
            'password': user_obj.password,
        }
        form = UserForm(data=init_dic)
        return render(request, "backend_user_read.html", {"form": form, "user_obj": user_obj, "uid": uid})


@check_login
def user_edit(request, uid):
    if request.method == "GET":
        user_obj = models.User.objects.filter(id=uid).first()
        init_dic = {
            'username': user_obj.username,
            'password': user_obj.password,
        }
        form = UserForm(data=init_dic)
        return render(request, "backend_user_edit.html", {"form": form, "user_obj": user_obj, "uid": uid})
    elif request.method == "POST":
        form = UserForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():  # 事务操作
                models.User.objects.filter(id=uid).update(**form.cleaned_data)
                return redirect("/backend/user/read-%s/" % uid)
        else:
            return render(request, "backend_user_edit.html", {"form": form})


@check_login
def user_delete(request):
    if request.method == "POST":
        del_id = request.POST.get("del_id")
        print(del_id)
        with transaction.atomic():  # 事务操作
            models.User.objects.filter(id=del_id).delete()
            return redirect("/backend/user/")


@check_login
def user_add(request):
    if request.method == "GET":
        form = UserForm()
        return render(request, "backend_user_add.html", {"form": form})
    if request.method == "POST":
        form = UserForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():  # 事务操作
                print(form.cleaned_data)
                models.User.objects.create(**form.cleaned_data)
                return redirect("/backend/user/")
        else:
            return render(request, "backend_user_add.html", {"form": form})


@check_login
def user_update(request):
    if request.method == "POST":
        ret = {"status": True, "data": None}
        new_pwd = request.POST.get("password")
        print(new_pwd)
        obj = models.User.objects.filter(username=request.session.get("username")).update(password=new_pwd)
        return HttpResponse(json.dumps(ret))


@check_login
def index(request):
    order_count = models.Order.objects.filter(deal=False).all().count()
    request.session["order_count"] = order_count
    return render(request, "backend_index.html")


@check_login
def home(request):
    path = os.getcwd() + "/static/images/lbt/"
    print(path)
    imgs = os.listdir(path)
    return render(request, "backend_home.html", {"imgs": imgs})


@check_login
def companyIntroduce(request):
    if request.method == "GET":
        company_obj = models.Company.objects.filter().first()
        init_dic = {
            'com_name': company_obj.com_name,
            'com_tel': company_obj.com_tel,
            'com_weChat': company_obj.com_weChat,
            'com_validity': company_obj.com_validity,
            'com_introduction': company_obj.com_introduction,
            'teach_idea': company_obj.teach_idea,
            'school_address': company_obj.school_address,
            'recruit': company_obj.recruit
        }
        form = CompanyForm(data=init_dic)
        return render(request, "backend_aboutAT.html", {"form": form})
    if request.method == "POST":
        com_introduction = request.POST.get("com_introduction")
        print(com_introduction)
        models.Company.objects.filter().update(com_introduction=com_introduction)
        return redirect("/backend/companyIntroduce/")


@check_login
def recruit(request):
    if request.method == "GET":
        company_obj = models.Company.objects.filter().first()
        init_dic = {
            'com_name': company_obj.com_name,
            'com_tel': company_obj.com_tel,
            'com_weChat': company_obj.com_weChat,
            'com_validity': company_obj.com_validity,
            'com_introduction': company_obj.com_introduction,
            'teach_idea': company_obj.teach_idea,
            'school_address': company_obj.school_address,
            'recruit': company_obj.recruit
        }
        form = CompanyForm(data=init_dic)
        return render(request, "backend_joinAT.html", {"form": form})
    if request.method == "POST":
        recruit = request.POST.get("recruit")
        print(recruit)
        models.Company.objects.filter().update(recruit=recruit)
        return redirect("/backend/recruit/")


@check_login
def teach(request):
    if request.method == "GET":
        company_obj = models.Company.objects.filter().first()
        init_dic = {
            'com_name': company_obj.com_name,
            'com_tel': company_obj.com_tel,
            'com_weChat': company_obj.com_weChat,
            'com_validity': company_obj.com_validity,
            'com_introduction': company_obj.com_introduction,
            'teach_idea': company_obj.teach_idea,
            'school_address': company_obj.school_address,
            'recruit': company_obj.recruit
        }
        form = CompanyForm(data=init_dic)
        return render(request, "backend_teachAT.html", {"form": form})
    if request.method == "POST":
        teach_idea = request.POST.get("teach_idea")
        print(recruit)
        models.Company.objects.filter().update(teach_idea=teach_idea)
        return redirect("/backend/teach/")


# @check_login
# def school(request):
#     if request.method == "GET":
#         company_obj = models.Company.objects.filter().first()
#         init_dic = {
#             'com_name': company_obj.com_name,
#             'com_tel': company_obj.com_tel,
#             'com_weChat': company_obj.com_weChat,
#             'com_validity': company_obj.com_validity,
#             'com_introduction': company_obj.com_introduction,
#             'teach_idea': company_obj.teach_idea,
#             'school_address': company_obj.school_address,
#             'recruit': company_obj.recruit
#         }
#         form = CompanyForm(data=init_dic)
#         return render(request, "backend_schoolAT.html", {"form": form})
#     if request.method == "POST":
#         school_address = request.POST.get("school_address")
#         print(school_address)
#         models.Company.objects.filter().update(school_address=school_address)
#         return redirect("/backend/school/")


@check_login
def baseinfo(request):
    if request.method == "GET":
        company_obj = models.Company.objects.filter().first()
        return render(request, "backend_baseinfoAT.html", {"company_obj": company_obj})


@check_login
def baseinfo_update(request):
    if request.method == "POST":
        ret = {"status": True, "data": None}
        com_name = request.POST.get("com_name")
        com_tel = request.POST.get("com_tel")
        com_validity = request.POST.get("com_validity")
        models.Company.objects.filter().update(
            com_name=com_name,
            com_tel=com_tel,
            com_validity=com_validity
        )
        return HttpResponse(json.dumps(ret))


@check_login
@xframe_options_exempt
def upload_avatar(request):
    avatarImg = request.FILES.get('avatarImg')
    print("hahaha", avatarImg)
    import os
    img_path = os.path.join('static/images', "we_Chat.jpg")
    print(img_path)
    with open(img_path, 'wb') as f:
        for item in avatarImg.chunks():
            f.write(item)

    models.Company.objects.filter().update(com_weChat="/"+img_path)

    ret = {'status': True, 'data': img_path}
    import json
    return HttpResponse(json.dumps(ret))


@check_login
@xframe_options_exempt
def upload_log(request):
    avatarImg = request.FILES.get('avatarImg2')
    print("hahaha", avatarImg)
    import os
    img_path = os.path.join('static/images', "com_log.jpg")
    print(img_path)
    with open(img_path, 'wb') as f:
        for item in avatarImg.chunks():
            f.write(item)

    models.Company.objects.filter().update(com_log="/"+img_path)

    ret = {'status': True, 'data': img_path}
    import json
    return HttpResponse(json.dumps(ret))


@check_login
@xframe_options_exempt
def upload_companyImg(request):
    avatarImg = request.FILES.get('avatarImg3')
    print("hahaha", avatarImg)
    import os
    img_path = os.path.join('static/images', "com_img.jpg")
    print(img_path)
    with open(img_path, 'wb') as f:
        for item in avatarImg.chunks():
            f.write(item)

    models.Company.objects.filter().update(com_img="/"+img_path)

    ret = {'status': True, 'data': img_path}
    import json
    return HttpResponse(json.dumps(ret))


@check_login
@xframe_options_exempt
def upload_img(request):
    #print(request.FILES["imgFile"], type(request.FILES))
    img_obj = request.FILES.get('imgFile')
    #print(type(img_obj.name))
    import os
    path = os.path.join('', 'static/images')
    img_path = os.path.join(path, str(img_obj.name))
    #print(img_path, type(img_path))
    with open(img_path, 'wb') as f:
        for item in img_obj.chunks():
            f.write(item)
    dic = {
        'error': 0,
        'url': '/'+img_path,
        'message': '错误了...'
    }
    print(img_path)

    print(base.BASE_DIR)
    return HttpResponse(json.dumps(dic))


@check_login
@xframe_options_exempt
def upload_lbt(request):
    #print(request.FILES["imgFile"], type(request.FILES))
    img_obj = request.FILES.get('fafafa')
    #print(type(img_obj.name))
    import os
    path = os.path.join('', 'static/images/lbt')
    img_path = os.path.join(path, str(img_obj.name))
    #print(img_path, type(img_path))
    with open(img_path, 'wb') as f:
        for item in img_obj.chunks():
            f.write(item)
    dic = {
        'error': 0,
        'url': '/'+img_path,
        'message': '错误了...'
    }
    print(img_path)

    #print(settings.BASE_DIR)
    return HttpResponse(json.dumps(dic))


@check_login
@xframe_options_exempt
def delete_lbt(request):
    if request.method == "POST":
        path = request.POST.get("path")
        print(request.POST)
        print("path is: ", path)
        x = re.search("static/images/lbt/.*\.\w*", path)
        print("x", x, type(x))
        os.remove(x.group())
        return HttpResponse(json.dumps("ok"))


@check_login
def competitionResult(request):
    if request.method == "GET":
        data_count = models.CompetitionResult.objects.filter().count()
        page_obj = Page(request.GET.get("p", 1), data_count, 10, 5)
        page_str = page_obj.page_str("/backend/competitionResult/")
        competitionResult_obj = models.CompetitionResult.objects.filter().all()[page_obj.start: page_obj.end]

        return render(request, "backend_competitionResult.html", {"data_count": data_count, "page_str": page_str, "competitionResult_obj": competitionResult_obj})


@check_login
def competitionResult_add(request):
    if request.method == "GET":
        form = CompetitionResultForm()
        return render(request, "backend_competitionResult_add.html", {"form": form})
    if request.method == "POST":
        img_name = request.POST.get("img_name")
        form = CompetitionResultForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():  # 事务操作
                print(form.cleaned_data)
                print(img_name)
                models.CompetitionResult.objects.create(**form.cleaned_data, cr_img = img_name)
                return redirect("/backend/competitionResult/")
        else:
            return render(request, "backend_competitionResult_add.html", {"form": form})


@check_login
@xframe_options_exempt
def upload_result_img(request):
    #print(request.FILES["imgFile"], type(request.FILES))
    img_obj = request.FILES.get('avatarImg')
    # img_name = request.POST.get("img_name")
    # img_name += ".jpg"
    # print("xuexue",img_name)
    #print(type(img_obj.name))
    import os
    path = os.path.join('', 'static/images/competitionResult')
    img_path = os.path.join(path, img_obj.name)
    #print(img_path, type(img_path))
    with open(img_path, 'wb') as f:
        for item in img_obj.chunks():
            f.write(item)
    ret = {'status': True, 'data': img_path}
    print(img_path)

    #print(settings.BASE_DIR)
    return HttpResponse(json.dumps(ret))


@check_login
def competitionResult_read(request, cid):
    if request.method == "GET":
        competitionResult_obj = models.CompetitionResult.objects.filter(id=cid).first()
        init_dic = {
            'cr_name': competitionResult_obj.cr_name,
            'cr_img': competitionResult_obj.cr_img,
        }
        form = CompetitionResultForm(data=init_dic)
        return render(request, "backend_competitionResult_read.html", {"form": form, "competitionResult_obj": competitionResult_obj, "cid": cid})


@check_login
def competitionResult_edit(request, cid):
    if request.method == "GET":
        competitionResult_obj = models.CompetitionResult.objects.filter(id=cid).first()
        init_dic = {
            'cr_name': competitionResult_obj.cr_name,
            'cr_img': competitionResult_obj.cr_img,
        }
        form = CompetitionResultForm(data=init_dic)
        return render(request, "backend_competitionResult_edit.html", {"form": form, "competitionResult_obj": competitionResult_obj, "cid": cid})
    elif request.method == "POST":
        form = CompetitionResultForm(data=request.POST)
        img_name = request.POST.get("img_name")
        if form.is_valid():
            with transaction.atomic():  # 事务操作
                models.CompetitionResult.objects.filter(id=cid).update(**form.cleaned_data, cr_img=img_name)
                return redirect("/backend/competitionResult/read-%s/" % cid)
        else:
            return render(request, "backend_competitionResult_edit.html", {"form": form})


@check_login
def competitionResult_delete(request):
    if request.method == "POST":
        del_id = request.POST.get("del_id")
        print(del_id)
        with transaction.atomic():  # 事务操作
            models.CompetitionResult.objects.filter(id=del_id).delete()
            return redirect("/backend/competitionResult/")

@check_login
def competition(request):
    if request.method == "GET":
        data_count = models.Competition.objects.filter().count()
        page_obj = Page(request.GET.get("p", 1), data_count, 10, 5)
        page_str = page_obj.page_str("/backend/competition/")
        competition_obj = models.Competition.objects.filter().all()[page_obj.start: page_obj.end]

        return render(request, "backend_competition.html", {"data_count": data_count, "page_str": page_str, "competition_obj": competition_obj})


@check_login
def competition_edit(request, cid):
    if request.method == "GET":
        competition_obj = models.Competition.objects.filter(id=cid).first()
        init_dic = {
            'com_name': competition_obj.com_name,
            'com_validity': competition_obj.com_validity,
            'com_introduction': competition_obj.com_introduction,
        }
        form = CompetitionForm(data=init_dic)
        return render(request, "backend_competition_edit.html", {"form": form, "competition_obj": competition_obj, "cid": cid})
    elif request.method == "POST":
        form = CompetitionForm(data=request.POST)
        img_name = request.POST.get("img_name")
        if form.is_valid():
            with transaction.atomic():  # 事务操作
                models.Competition.objects.filter(id=cid).update(**form.cleaned_data, com_img=img_name)
                return redirect("/backend/competition/read-%s/" % cid)
        else:
            return render(request, "backend_competition_edit.html", {"form": form})


@check_login
def competition_read(request, cid):
    if request.method == "GET":
        competition_obj = models.Competition.objects.filter(id=cid).first()
        init_dic = {
            'com_name': competition_obj.com_name,
            'com_validity': competition_obj.com_validity,
            'com_introduction': competition_obj.com_introduction,
        }
        form = CompetitionForm(data=init_dic)
        return render(request, "backend_competition_read.html", {"form": form, "competition_obj": competition_obj, "cid": cid})


@check_login
def competition_add(request):
    if request.method == "GET":
        form = CompetitionForm()
        return render(request, "backend_competition_add.html", {"form": form})
    if request.method == "POST":
        img_name = request.POST.get("img_name")
        form = CompetitionForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():  # 事务操作
                print(form.cleaned_data)
                print(img_name)
                models.Competition.objects.create(**form.cleaned_data, com_img = img_name)
                return redirect("/backend/competition/")
        else:
            return render(request, "backend_competition_add.html", {"form": form})


@check_login
def competition_delete(request):
    if request.method == "POST":
        del_id = request.POST.get("del_id")
        print(del_id)
        with transaction.atomic():  # 事务操作
            models.Competition.objects.filter(id=del_id).delete()
            return redirect("/backend/competition/")


@check_login
@xframe_options_exempt
def upload_competition_img(request):
    #print(request.FILES["imgFile"], type(request.FILES))
    img_obj = request.FILES.get('avatarImg')
    # img_name = request.POST.get("img_name")
    # img_name += ".jpg"
    # print("xuexue",img_name)
    #print(type(img_obj.name))
    import os
    path = os.path.join('', 'static/images')
    img_path = os.path.join(path, img_obj.name)
    #print(img_path, type(img_path))
    with open(img_path, 'wb') as f:
        for item in img_obj.chunks():
            f.write(item)


    ret = {'status': True, 'data': img_path}
    print(img_path)

    # print(settings.BASE_DIR)
    return HttpResponse(json.dumps(ret))


@check_login
def school(request):
    if request.method == "GET":
        data_count = models.School.objects.filter().count()
        page_obj = Page(request.GET.get("p", 1), data_count, 10, 5)
        page_str = page_obj.page_str("/backend/school/")
        school_obj = models.School.objects.filter().all()[page_obj.start: page_obj.end]

        return render(request, "backend_school.html", {"data_count": data_count, "page_str": page_str, "school_obj": school_obj})


@check_login
def school_add(request):
    if request.method == "GET":
        form = SchoolForm()
        return render(request, "backend_school_add.html", {"form": form})
    if request.method == "POST":
        form = SchoolForm(data=request.POST)
        #img_name = request.POST.get("img_name")
        if form.is_valid():
            with transaction.atomic():  # 事务操作
                print(form.cleaned_data)
                models.School.objects.create(**form.cleaned_data)
                return redirect("/backend/school/")
        else:
            return render(request, "backend_school_add.html", {"form": form})


@check_login
def school_read(request, sid):
    if request.method == "GET":
        school_obj = models.School.objects.filter(id=sid).first()
        init_dic = {
            'sc_name': school_obj.sc_name,
            'sc_addr': school_obj.sc_addr,
            'sc_tel': school_obj.sc_tel,
            'sc_environment': school_obj.sc_environment,
        }
        form = SchoolForm(data=init_dic)
        return render(request, "backend_school_read.html", {"form": form, "school_obj": school_obj, "sid": sid})


@check_login
def school_edit(request, sid):
    if request.method == "GET":
        school_obj = models.School.objects.filter(id=sid).first()
        init_dic = {
            'sc_name': school_obj.sc_name,
            'sc_addr': school_obj.sc_addr,
            'sc_tel': school_obj.sc_tel,
            'sc_environment': school_obj.sc_environment,
        }
        form = SchoolForm(data=init_dic)
        return render(request, "backend_school_edit.html", {"form": form, "school_obj": school_obj, "sid": sid})
    elif request.method == "POST":
        form = SchoolForm(data=request.POST)
        if form.is_valid():
            with transaction.atomic():  # 事务操作
                models.School.objects.filter(id=sid).update(**form.cleaned_data)
                return redirect("/backend/school/read-%s/" % sid)
        else:
            return render(request, "backend_school_edit.html", {"form": form})


@check_login
def school_delete(request):
    if request.method == "POST":
        del_id = request.POST.get("del_id")
        print(del_id)
        with transaction.atomic():  # 事务操作
            models.School.objects.filter(id=del_id).delete()
            return redirect("/backend/school/")


@check_login
def course(request):
    if request.method == "GET":
        data_count = models.Course.objects.filter().count()

        page_obj = Page(request.GET.get("p", 1), data_count, 10, 5)
        page_str = page_obj.page_str("/backend/course/")
        course_obj = models.Course.objects.filter().all()[page_obj.start: page_obj.end]
        return render(request, "backend_course.html", {"data_count": data_count, "course_obj": course_obj, "page_str": page_str})


@check_login
def course_read(request, cid):
    if request.method == "GET":
        course_obj = models.Course.objects.filter(id=cid).first()
        init_dic = {
            'cour_name': course_obj.cour_name,
            'cour_validity': course_obj.cour_validity,
            'cour_introduction': course_obj.cour_introduction,
        }
        form = CourseForm(data=init_dic)
        return render(request, "backend_course_read.html", {"form": form, "course_obj": course_obj, "cid": cid})


@check_login
def course_edit(request, cid):
    if request.method == "GET":
        course_obj = models.Course.objects.filter(id=cid).first()
        init_dic = {
            'cour_name': course_obj.cour_name,
            'cour_validity': course_obj.cour_validity,
            'cour_introduction': course_obj.cour_introduction,
        }
        form = CourseForm(data=init_dic)
        return render(request, "backend_course_edit.html", {"form": form, "course_obj": course_obj, "cid": cid})
    elif request.method == "POST":
        form = CourseForm(data=request.POST)
        img_name = request.POST.get("img_name")
        if form.is_valid():
            with transaction.atomic():  # 事务操作
                models.Course.objects.filter(id=cid).update(**form.cleaned_data, cour_img=img_name)
                return redirect("/backend/course/read-%s/" % cid)
        else:
            return render(request, "backend_course_edit.html", {"form": form})


@check_login
def course_delete(request):
    if request.method == "POST":
        del_id = request.POST.get("del_id")
        print(del_id)
        with transaction.atomic():  # 事务操作
            models.Course.objects.filter(id=del_id).delete()
            return redirect("/backend/course/")


@check_login
def course_add(request):
    if request.method == "GET":
        form = CourseForm()
        return render(request, "backend_course_add.html", {"form": form})
    if request.method == "POST":
        form = CourseForm(data=request.POST)
        img_name = request.POST.get("img_name")
        if form.is_valid():
            with transaction.atomic():  # 事务操作
                print(form.cleaned_data)
                models.Course.objects.create(**form.cleaned_data, cour_img=img_name)
                return redirect("/backend/course/")
        else:
            return render(request, "backend_course_add.html", {"form": form})


@check_login
@xframe_options_exempt
def upload_course_img(request):
    #print(request.FILES["imgFile"], type(request.FILES))
    img_obj = request.FILES.get('avatarImg')
    # img_name = request.POST.get("img_name")
    # img_name += ".jpg"
    # print("xuexue",img_name)
    #print(type(img_obj.name))
    import os
    path = os.path.join('', 'static/images')
    img_path = os.path.join(path, img_obj.name)
    #print(img_path, type(img_path))
    with open(img_path, 'wb') as f:
        for item in img_obj.chunks():
            f.write(item)


    ret = {'status': True, 'data': img_path}
    print(img_path)

    #print(settings.BASE_DIR)
    return HttpResponse(json.dumps(ret))


@check_login
def logout(request):
    request.session.flush()
    return redirect('/login/')
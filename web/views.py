from django.shortcuts import render, HttpResponse, redirect
from database import models
from web.forms.order import OrderForm
from web.forms.user import UserForm
from io import BytesIO
from utils.check_code import create_validate_code
import os, json, re

# Create your views here.


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')  # 图片信息写入内存
    request.session['checkCode'] = code
    return HttpResponse(stream.getvalue())  # 从内存中读取图片信息


def index(request):
    """
    首页
    :param request:
    :return:
    """
    path = os.getcwd() + "/static/images/lbt/"
    print(path)
    imgs = os.listdir(path)
    company_obj = models.Company.objects.filter().first()
    competitions = models.Competition.objects.filter().all()[:3]
    courses = models.Course.objects.filter().all()
    return render(request, "index.html", {"company_obj": company_obj, "path": path, "imgs": imgs, "competitions": competitions, "courses": courses})

def order(request):
    """
    试听课预约
    :param request:
    :return:
    """
    if request.method == "GET":
        obj = OrderForm()
        company_obj = models.Company.objects.filter().first()
        return render(request, "order.html", {"obj": obj, "company_obj": company_obj})
    elif request.method == "POST":
        obj = OrderForm(request.POST)
        company_obj = models.Company.objects.filter().first()
        if obj.is_valid():
            print(obj.cleaned_data)
            stu_name = request.POST.get("stu_name", None)
            weChat = request.POST.get("weChat", None)
            print(stu_name, weChat)
            checkCode = request.POST.get("check_code")
            if checkCode.upper() == request.session.get("checkCode").upper():
                order_obj = models.Order.objects.filter(telephone=obj.cleaned_data["telephone"]).first()
                if order_obj:
                    return render(request, "order_result.html", {"result": "您已预约成功，请勿重复操作", "company_obj": company_obj})
                models.Order.objects.create(stu_name=stu_name, weChat=weChat, **obj.cleaned_data)
                return render(request, "order_result.html", {"result": "恭喜您，预约成功，请耐心等待教务老师的联系", "company_obj": company_obj})
            else:
                return render(request, "order.html", {"obj": obj, "checkError": "验证码错误", "company_obj": company_obj})
        else:
            print("hhhh")
            return render(request, "order.html", {"obj": obj, "company_obj": company_obj})
    return render(request, "order.html")


def orderr(request):
    """
    试听课预约
    :param request:
    :return:
    """
    # if request.method == "GET":
    #     obj = OrderForm()
    #     company_obj = models.Company.objects.filter().first()
    #     return render(request, "order.html", {"obj": obj, "company_obj": company_obj})
    # el
    if request.method == "POST":
        ret = {'code': 0}
        stu_tel = request.POST.get("stu_tel")
        stu_name = request.POST.get("stu_name", None)
        stu_age = request.POST.get("stu_age")
        print("hahaha content:", stu_tel, stu_age, stu_name)
        phone_pat = re.search("[0-9]{11}", stu_tel)
        if not phone_pat:
            #if not phone_pat.group():
            ret["tel_err"] = "手机号码格式不对，请输入11位手机号码"
            return HttpResponse(json.dumps(ret))
        else:
            ret["tel_err"] = ""
        if not stu_name:
            ret["name_err"] = "请输入孩子的称呼"
            return HttpResponse(json.dumps(ret))
        else:
            ret["name_err"] = ""
        if not stu_age:
            ret["age_err"] = "请输入孩子的年龄"
            return HttpResponse(json.dumps(ret))
        else:
            ret["age_err"] = ""

        order_obj = models.Order.objects.filter(telephone=stu_tel).first()
        if order_obj:
            ret["tel_err"] = "该手机号码已经预约过，请勿重复操作"
            return HttpResponse(json.dumps(ret))
        else:
            models.Order.objects.create(stu_name=stu_name, stu_age=stu_age, telephone=stu_tel)
            ret["code"] = 1
            return HttpResponse(json.dumps(ret))


def about(request):
    """
    AT介绍
    :param request:
    :return:
    """
    if request.method == "GET":
        company_obj = models.Company.objects.filter().first()
        school_obj = models.School.objects.filter().all()
        print(request.path_info)
        return render(request, "company_profile_layout.html", {"company_obj": company_obj, "school_obj": school_obj})

def course(request, cid):
    """
    课程体系
    :param request:
    :return:
    """
    course_obj = models.Course.objects.filter().all()
    now_course_obj = models.Course.objects.filter(id=cid).first()
    school_obj = models.School.objects.filter().all()
    if not now_course_obj:
        now_course_obj = models.Course.objects.filter().first()
    company_obj = models.Company.objects.filter().first()
    return render(request, "course.html", {"course_obj": course_obj, "company_obj": company_obj, "now_course_obj": now_course_obj, "school_obj": school_obj})


def competition(request, cid):
    """
    比赛项目
    :param request:
    :return:
    """
    competition_obj = models.Competition.objects.filter().all()
    now_competition_obj = models.Competition.objects.filter(id=cid).first()
    school_obj = models.School.objects.filter().all()
    if not now_competition_obj:
        now_competition_obj = models.Competition.objects.filter().first()
    company_obj = models.Company.objects.filter().first()
    return render(request, "competition.html", {"competition_obj": competition_obj, "company_obj": company_obj, "now_competition_obj": now_competition_obj, "school_obj": school_obj})


def login(request):
    """
    登录管理员账号
    :param request:
    :return:
    """
    if request.method == "GET":
        obj = UserForm()
        return render(request, "login.html", {"obj": obj})
    elif request.method == "POST":
        obj = UserForm(request.POST)
        r1 = obj.is_valid()
        if r1:
            user_obj = models.User.objects.filter(**obj.cleaned_data)
            if user_obj:
                request.session['username'] = obj.cleaned_data['username']
                return redirect("/backend/index/")
            else:
                return render(request, "login.html", {"obj": obj, "user_err": "用户名或密码错误"})
        else:
            # print(obj.errors["user"][0])
            return render(request, "login.html", {"obj": obj})


def register(request):
    """
    注册管理员账号
    :param request:
    :return:
    """
    if request.method == "GET":
        obj = UserForm()
        return render(request, "register.html", {"obj": obj})


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')  # 图片信息写入内存
    request.session['checkCode'] = code
    return HttpResponse(stream.getvalue())  # 从内存中读取图片信息
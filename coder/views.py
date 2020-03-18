from django.shortcuts import render
from .models import *
from .sendVerCode import codeSender
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.clickjacking import xframe_options_exempt
import random

def wrong(func):
    def wrap(request, *args, **kwargs):
        try:
            return func(request, *args, **kwargs)
        except Exception:
            return HttpResponse("未知错误")
    return wrap

# Create your views here.

sender = codeSender()

@wrong
@xframe_options_exempt      # 去掉frame限制
def codePage(request, ansID):
    try:
        ans = Answer.objects.get(id=ansID)
    except Answer.DoesNotExist:
        return HttpResponse("ID Error")
    return render(request, "empty.html", {"code": ans.content})

@wrong
def loginOut(request):
    logout(request)
    return redirect("/")
    
@wrong
def register(request):
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    verCode = request.POST.get("verCode")
    if username:
        try:
            v = VerCode.objects.get(email=email)
            if str(v.code) == verCode:
                try:
                    User.objects.get(username=username)
                    return render(request, "register.html", context={"info": "用户已存在"})
                except User.DoesNotExist:
                    User.objects.create_user(username=username, password=password, email=email)
                    VerCode.objects.get(email=email).delete()
                    return render(request, "login.html", {"mess": "注册成功"})
            else:
                return render(request, "register.html", context={"info": "验证码错误"})
        except VerCode.DoesNotExist:
            return render(request, "register.html", context={"info": "请获取验证码"})
    else:
        return render(request ,"register.html")

# 发送验证码
@wrong
def verCode(request, **kwargs):
    email = request.GET.get("email")
    if kwargs.get("type") == "1":     # 重置密码
        try:
            u = User.objects.filter(email=email)
            assert u.count() != 0
        except AssertionError:
            return HttpResponse("该邮箱未注册")
    else:
        try:
            u = User.objects.filter(email=email)
            assert u.count() > 0
            return HttpResponse("该邮箱已注册")
        except AssertionError:
            pass

    # 卡发送时间
    try:
        eCode = VerCode.objects.get(email=email)
        if (timezone.now() - eCode.time).seconds <= 60:
            return HttpResponse("发送间隔太小，请等会再尝试")
    except VerCode.DoesNotExist:
        pass
    
    # 随机生成验证码
    code = ''.join([str(random.randint(0,9)) for i in range(6)])
    # 调用发送模块
    res = sender.send(email, code)
    if "成功" in res:
        try:
            v = VerCode.objects.get(email=email)
            v.code = code
            v.time = timezone.now()
            v.save()
        except VerCode.DoesNotExist:
            VerCode(email=email, code=code, time=timezone.now()).save()
    return HttpResponse(res)

@wrong
def blogLogin(request):
    # 登录验证
    if str(request.user) != "AnonymousUser":
        return redirect("/")
    username = request.POST.get('username')
    password = request.POST.get("password")
    next_ = request.GET.get("next")
    if username:
        user = authenticate(username=username, password=password)
        mess = ""
        if user:
            login(request, user)
            if next_:
                return redirect(next_)
            return redirect("/")
        else:
            try:
                # 使用邮箱验证
                user = User.objects.get(email=username)
                if user.check_password(password):
                    user = authenticate(username=user.username, password=password)
                    login(request, user)
                    if next_:
                        return redirect(next_)
                    return redirect("/")
                mess = "用户名或密码错误"
            except User.DoesNotExist:
                mess = "用户名或密码错误"
        return render(request, "login.html", context={"mess": mess})
    else:
        return render(request, "login.html")

# 重置密码
@wrong
def resetPassword(request):
    email = request.POST.get("email")
    verCode = request.POST.get("verCode")
    password = request.POST.get("password")
    mes = ""
    try:
        code = VerCode.objects.get(email=email)
        if str(code.code) == str(verCode):      # 通过验证
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            code.delete()
            return render(request, "login.html", context={"mess": "密码重置成功"})
        else:
            mes = "验证码错误"
    except VerCode.DoesNotExist:
        mes = "请先获取验证码"
    except User.DoesNotExist:
        mes = "邮箱未注册"
    if email:
        return render(request, "resetPassword.html", context={"mes": mes})
    else:
        return render(request, "resetPassword.html")
    
@wrong
@login_required
def getQuestion(request, Qid):
    try:
        question = Question.objects.get(id=Qid)
    except Question.DoesNotExist:
        return HttpResponse("id错误")
    return render(request, "question.html", {"question": question})

@wrong
@login_required
def userSet(request):
    user = request.user
    return render(request, "userSet.html", {"user": user})


@wrong
@login_required
def index(request):
    questions = [model_to_dict(i) for i in Question.objects.all()]
    return render(request, "index.html", {"questions": questions})

@wrong
@login_required
def resetName(request):
    user = request.user
    try:
        user.username = request.POST.get("username")
        mes = "修改成功"
        user.save()
    except:
        mes = "用户名已存在"
    return render(request, "userSet.html", {"info": mes})

@wrong
# @login_required
def showCode(request, Cid):
    try:
        ans = Answer.objects.get(id=Cid)
    except Answer.DoesNotExist:
        return HttpResponse("id错误")
    return render(request, "showCode.html", {'code': ans})


# @wrong
# @login_required
def codeList(request):
    if str(request.user) == "AnonymousUser":
        isLogined = False
    else:
        isLogined = True
    codes = [{
        "id": i.id,
        "title": i.user.username+"-"+i.question.title
    } for i in Answer.objects.all()]
    return render(request, "codeList.html", {"codes": codes, "isLogined": isLogined})

@wrong
@login_required
def submitAnswer(request):
    try:
        question = Question.objects.get(id=request.POST.get("Qid"))
    except Question.DoesNotExist:
        return HttpResponse("id错误")
    if timezone.now() > question.endTime:
        return render(request, "question.html", {"info": "已过提交时间", "question": question})
    content = request.POST.get('code')
    if not content.strip():
        return render(request, "question.html", {"info": "空白提交，驳回重写", "question": question})
    try:
        ans = Answer.objects.get(user=request.user, question=question)
    except Answer.DoesNotExist:
        ans = Answer(user=request.user, question=question)
    ans.content = content
    ans.time = timezone.now()
    ans.save()
    return render(request, "question.html", {"info": "提交成功", "question": question})
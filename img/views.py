from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from hashlib import md5
from django.http import HttpResponse
from .models import *
import os
imgDir = os.path.join("static", "img")
# 域名
domain = "http://127.0.0.1:8000"

def imgIndex(request):
    imgs = Img.objects.all()
    return render(request, "img.html", {"imgs": [i.url for i in imgs]})

@csrf_exempt
def uploadImg(request):
    fd = request.FILES['pic'].read()
    name = md5(fd).hexdigest()
    # 在数据库中查找文件，确保文件只上传一次
    try:
        img = Img.objects.get(imgMD5=name)
    except Img.DoesNotExist:
        # 写入图片
        with open(os.path.join(imgDir, f"{name}.jpg"), "wb") as f:
            f.write(fd)
        img = Img(imgMD5=name, url=f'{domain}/static/img/{name}.jpg')
        img.save()
    return HttpResponse(img.url)
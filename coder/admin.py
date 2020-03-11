from django.contrib import admin

from .models import *

admin.site.register(VerCode)
admin.site.register(Answer)
admin.site.register(Question)

# Register your models here.

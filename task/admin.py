from django.contrib import admin

from .models import Task, Logs
# Register your models here.
admin.site.register(Task)
admin.site.register(Logs)
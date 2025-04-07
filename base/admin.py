from django.contrib import admin
from base.models import Task, UserProfile, UserTask


admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(UserTask)

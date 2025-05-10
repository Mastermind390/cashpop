from django.contrib import admin
from base.models import Task, UserProfile, UserTask, UserAccountDetail, Withdrawal, Top_up, Subscription


admin.site.register(Task)
admin.site.register(UserProfile)
admin.site.register(UserTask)
admin.site.register(UserAccountDetail)
admin.site.register(Withdrawal)
admin.site.register(Top_up)
admin.site.register(Subscription)

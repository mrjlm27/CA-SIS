from django.contrib import admin
from .models import *
# Register your models here.
# class AccountAdmin(admin.ModelAdmin):
#     list_display=['username','password']

# class StudentAdmin(admin.ModelAdmin):
#     list_display=['s_name']

# class TeacherAdmin(admin.ModelAdmin):
#     list_display=['t_name']

# admin.site.register(Account)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Payment)
admin.site.register(TranscriptOfRecord)
admin.site.register(GradeReport)
admin.site.register(Announcement)


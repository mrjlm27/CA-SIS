from django.urls import path
from django.conf import settings
from . import views


app_name = 'sis_app'

urlpatterns=[
    path('studentList',views.StudentList, name="student_list"),
    path('studentForm',views.studentForm, name="student_form"),
    path('RegistrationList',views.RegistrationList, name="registration_list"),
    path('GenerateAccount/<int:id>',views.GenerateAccount, name="generate_account"),
    path('studentEnrollment',views.StudentEnrollment, name="student_enrollment"),
    # path('studentEnrollmentForm',views.studentEnrollmentForm, name="student_enrollment_form"),
]

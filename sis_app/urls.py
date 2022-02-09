from django.urls import path
from django.conf import settings
from . import views


app_name = 'sis_app'

urlpatterns=[
    path('', views.LogInScreen, name="log_in"),
    path('home',views.Home, name='home'),
    path('editAccount', views.EditAccountCred, name='edit_acc'),
    path('studentList',views.StudentList, name="student_list"),
    path('studentForm',views.studentForm, name="student_form"),
    path('RegistrationList',views.RegistrationList, name="registration_list"),
    path('GenerateAccount/<int:id>',views.GenerateAccount, name="generate_account"),
    path('paymentForm',views.paymentForm, name="payment_form"),
    path('paymentList',views.paymentList, name="payment_list"),
    path('resetBiAnnually',views.resetBAEnrollmentStatus, name="reset_BA"),
    path('resetQuarterly',views.resetQEnrollmentStatus, name="reset_Q"),
    path('resetAll',views.resetALLEnrollmentStatus, name="reset_ALL"),
    path('studentEnrollment',views.EnrollmentStatusAndPaymentPlan, name="student_enrollment"),
    path('GradeReportListNursery',views.GradeReportList_Nursery, name="grade_report_nursery"),
    path('GradeReportFormNursery/<int:id>',views.GradeReportFormNursery, name="grade_report_form_nursery"),


]

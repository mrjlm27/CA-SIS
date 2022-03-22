from django.urls import path
from django.conf import settings
from . import views


app_name = 'sis_app'

urlpatterns=[
    path('login', views.LogInScreen, name="log_in"),
    path('home',views.Home, name='home'),
    path('editAccount', views.EditAccountCred, name='edit_acc'),
    path('studentList',views.StudentList, name="student_list"),
    path('studentForm/<int:id>',views.studentForm, name="student_form"),
    path('RegstudentForm/<int:id>',views.RegstudentForm, name="reg_student_form"),
    # path('studentFormMidYr/<int:id>',views.disabledstudentForm, name="disabled_student_form"),
    path('RegistrationList',views.RegistrationList, name="registration_list"),
    path('GenerateAccount/<int:id>',views.GenerateAccount, name="generate_account"),
    path('paymentForm',views.paymentForm, name="payment_form"),
    path('paymentList',views.paymentList, name="payment_list"),
    path('resetBiAnnually',views.resetBAEnrollmentStatus, name="reset_BA"),
    path('resetQuarterly',views.resetQEnrollmentStatus, name="reset_Q"),
    path('resetAll',views.resetALLEnrollmentStatus, name="reset_ALL"),
    path('studentEnrollment',views.EnrollmentStatusAndPaymentPlan, name="student_enrollment"),
    path("StudentPaymentView", views.StudentPaymentView, name = "student_paymentview"),
    path('GradeReportListNursery',views.GradeReportList_Nursery, name="grade_report_nursery"),
    path('GradeReportFormNursery/<int:id>',views.GradeReportFormNursery, name="grade_report_form_nursery"),
    path('GradeReportListKinder2Senior',views.GradeReportList_Kinder2Senior, name="grade_report_kinder2senior"),
    path('GradeReportFormKinder2Senior/<int:id>',views.GradeReportFormKinder2Senior, name="grade_report_form_kinder2senior"),
    path('GradeReportListKinder1Kinder2Junior',views.GradeReportList_Kinder1Kinder2Junior, name="grade_report_k1k2jr"),
    path('GradeReportFormKinder1Kinder2Junior/<int:id>',views.GradeReportFormKinder1Kinder2Junior, name="grade_report_form_k1k2jr"),
    path('GenerateTOR/<int:id>', views.generateTOR, name= 'generate_tor'), 
    path('ViewGradeReport',views.viewGradeReport, name = "viewGradeReport"),
    path('Admin_EditAccount/<int:id>',views.EditAccountCred_admin, name = "admin_account_edit"),
    path('Delete_Button',views.deleteStudentsPage, name = "delete_students_page"),
    path('Delete_Students',views.deleteStudents, name = "delete_students"),
    path('ToggleRegistration',views.toggleRegistration, name = "toggle_registration"),
    path('logout', views.logout, name="log_out"),
]

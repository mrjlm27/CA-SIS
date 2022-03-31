from asyncore import read
from audioop import avg
from email import header
from multiprocessing import context
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import json
import datetime
from django.http import JsonResponse
from .models import *
from .forms import *
from .filters import *
from django.contrib.auth.models import User
import random
import string
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from datetime import date
import io
import reportlab
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import Table, SimpleDocTemplate, BaseDocTemplate, TableStyle
from reportlab.lib import colors, fonts
from reportlab.pdfgen import canvas
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.password_validation import validate_password


# GLOBAL VARIABLES
toggle = True #used for enabling/disabling student registration

# def hello_world(request):
#     return render(request, 'sis_app/hello_world.html')
@login_required(login_url='sis_app:log_in')
def Home(request):
    # announcement_list = Announcement.objects.all()
    # print(len(announcement_list))
    try:
        announcement = Announcement.objects.latest('id')
        context={'announcement':announcement}
        if request.user.is_superuser:
            return render(request,'sis_app/home_admin.html',context)
        else:
            return render(request,'sis_app/home.html',context)
    except ObjectDoesNotExist:
        if request.user.is_superuser:
            return render(request,'sis_app/home_admin_no_announcements.html')
        else:
            return render(request, 'sis_app/home_no_announcements.html')



def LogInScreen(request):
    id = 0
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password)
        if user is not None: #If log-in credentials are correct
            login(request, user)
            return redirect('/home')
        else: #if log-in creds are incorrect
            print('hello')
            messages.error(request, "Username or Password is incorrect")
    context = {'id':id}
    return render(request, 'sis_app/LogIn.html', context)

@login_required(login_url='sis_app:log_in')
def announcement_form(request, id=0):
    model = Announcement
    form_class = AnnouncementForm
    if request.method == "GET":
        if id == 0: 
            form = AnnouncementForm()
        else:
            announcement = Announcement.objects.get(pk=id)
            form = AnnouncementForm(instance=announcement)
        return render(request,"sis_app/home_announcement_form.html",{'form':form})
    else:
        if id == 0:
            form = AnnouncementForm(request.POST)
        else:
            announcement = Announcement.objects.get(pk=id)
            form = AnnouncementForm(request.POST,instance=announcement)
        if form.is_valid():
            form.save()
        return redirect('sis_app:home')

@login_required(login_url='sis_app:log_in')
def EditAccountCred(request):
    # user = User.objects.get(username=request.username, password=request.password)
    # if request.user.is_authenticated():
    if request.method == 'POST':
        old_u = request.user.username
        old_p = request.user.password
        user = User.objects.get(username=old_u,password=old_p)
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        if User.objects.filter(username=new_username).exists():
                messages.error(request,'username taken', extra_tags='username')
                return redirect(f'/editAccount')
        else:
            try:
                validate_password(new_password)
                # user.set_username(new_username)
                user_id = request.user.id
                student_entity = Student.objects.get(pk = user_id)
                student_entity.username = new_username
                student_entity.password = make_password(new_password)
                student_entity.save()
                user.username = new_username
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Account Details successfully changed. Please login again.')
                return redirect('sis_app:log_in')
            except ValidationError:
                messages.error(request, 'error', extra_tags='password')
                return redirect(f'/editAccount')
    context={}
    return render(request, 'sis_app/Account_Edit.html', context)

@login_required(login_url='sis_app:log_in')
def EditAccountCred_admin(request,id):
    if request.user.is_superuser:
        if request.method == 'POST':
            user_entity = User.objects.get(pk = id)
            new_username = request.POST.get('username')
            new_password = request.POST.get('password')
            # user.set_username(new_username)
            student_entity = Student.objects.get(pk = id)
            student_entity.username = new_username
            student_entity.password = new_password

            #sending new user and pass to student via email
            send_mail(
                        'CAMELEAN ACADEMY SIS CHANGE OF USERNAME AND PASSWORD',
                        "Username: {}\nPassword: {}\nPLEASE CHANGE YOUR USERNAME AND PASSWORD UPON LOGGING IN".format(student_entity.username, student_entity.password),
                        None,
                        ['gmgtechdev@gmail.com'],#this is the recipient(change this to email of student later)[student_entity.email]
                        fail_silently=False,
                    )

            student_entity.password = make_password(new_password)
            student_entity.save()
            user_entity.username = new_username
            user_entity.set_password(new_password)
            user_entity.save()
            return redirect('sis_app:student_list')
        context={}
        return render(request, 'sis_app/Admin_Account_Edit.html', context)
    else:
        return redirect('sis_app:home')

@login_required(login_url='sis_app:log_in')
def StudentList(request):
    if request.user.is_superuser:
        global toggle
        print(toggle)
        students = Student.objects.all()
        myFilter = StudentFilter(request.GET, queryset=students)
        students = myFilter.qs
        # toggle = 
        if toggle == True: #toggle is a global variable
            caption = 'Disable Registration'
        else:
            caption = 'Enable Registration'
        context = {'studentList' : students, 'myFilter': myFilter, 'caption':caption}
        return render(request,"sis_app/Student_List.html", context)
    else:
        return redirect('sis_app:home')


@login_required(login_url='sis_app:log_in')
def toggleRegistration(request):
    if request.user.is_superuser:
        # global toggle
        # print(toggle)
        # students = Student.objects.all()
        # myFilter = StudentFilter(request.GET, queryset=students)
        # students = myFilter.qs
        # if toggle == True: #toggle is a global variable
        #     caption = 'Disable Registration'
        #     toggle = False
        # else:
        #     caption = 'Enable Registration'
        #     toggle = True
        # context = {'studentList' : students, 'myFilter': myFilter, 'caption':caption}
        # return render(request,"sis_app/Student_List.html", context)
        global toggle
        if toggle == True: #toggle is a global variable
            # caption = 'Disable Registration'
            toggle = False
        else:
            # caption = 'Enable Registration'
            toggle = True
        # context = {'caption':caption}
        return render(request,"sis_app/home_admin.html")
    else:
        return redirect('sis_app:home')


def RegstudentForm(request,id = 0):
    model = Student
    form_class = StudentForm
    if request.method == "GET":
        if id == 0: 
            form = StudentForm()
        else:
            student = Student.objects.get(pk=id)
            form = StudentForm(instance=student)
        return render(request,"sis_app/Student_Form.html",{'form':form})
    else:
        if id == 0:
            form = StudentForm(request.POST)
        else:
            student = Student.objects.get(pk=id)
            form = StudentForm(request.POST,instance=student)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, 'error', extra_tags='reginvalidemail')
            return redirect(f'/RegstudentForm/{id}')
        messages.success(request, 'Account Successfully Created. Please wait for account details in your registered email')
        return redirect('sis_app:log_in')   
    context = {'form': form_class}
    context = {'form':form_class, 'student':model}
    return render(request, 'sis_app/Student_Form.html', context)

@login_required(login_url='sis_app:log_in')
def studentForm(request,id=0):
    global toggle
    print(toggle)
    if toggle == True:
        model = Student
        form_class = StudentForm
        if request.method == "GET":
            if id == 0: 
                form = StudentForm()
            else:
                student = Student.objects.get(pk=id)
                form = StudentForm(instance=student)
            return render(request,"sis_app/Student_Form.html",{'form':form})
        else:
            if id == 0:
                form = StudentForm(request.POST)
            else:
                student = Student.objects.get(pk=id)
                form = StudentForm(request.POST,instance=student)
            if form.is_valid():
                form.save()
                return redirect('sis_app:home')   
            else:
                messages.error(request, 'error', extra_tags='invalidemail')
                return redirect(f'/studentForm/{id}')
        context = {'form': form_class}
        context = {'form':form_class, 'student':model}
        return render(request, 'sis_app/Student_Form.html', context)
    elif toggle == False:
        model = Student
        form_class = StudentFormDisabled
        if request.method == "GET":
            if id == 0: 
                form = StudentFormDisabled()
            else:
                student = Student.objects.get(pk=id)
                f_name = student.student_firstname
                l_name = student.student_lastname
                grade_level = student.student_grade_level
                form = StudentFormDisabled(instance=student)
                context = {'form':form, 'f_name':f_name, 'l_name':l_name, 'grade_level':grade_level}
            return render(request,"sis_app/Student_Form_disabled.html",context)
        else:
            if id == 0:
                form = StudentFormDisabled(request.POST)
            else:
                student = Student.objects.get(pk=id)
                form = StudentFormDisabled(request.POST,instance=student)
            if form.is_valid():
                form.save()
                return redirect('sis_app:home')  
            else:
                messages.error(request, 'error',extra_tags='invalidemail')
                return redirect(f'/studentForm/{id}')
             


# def disabledstudentForm(request,id=0):
#     model = Student
#     form_class = StudentFormDisabled
#     if request.method == "GET":
#         if id == 0: 
#             form = StudentFormDisabled()
#         else:
#             student = Student.objects.get(pk=id)
#             f_name = student.student_firstname
#             l_name = student.student_lastname
#             grade_level = student.student_grade_level
#             form = StudentFormDisabled(instance=student)
#             context = {'form':form, 'f_name':f_name, 'l_name':l_name, 'grade_level':grade_level}
#         return render(request,"sis_app/Student_Form_disabled.html",context)
#     else:
#         if id == 0:
#             form = StudentFormDisabled(request.POST)
#         else:
#             student = Student.objects.get(pk=id)
#             form = StudentFormDisabled(request.POST,instance=student)
#         if form.is_valid():
#             form.save()
#         return redirect('sis_app:log_in')
#     # context = {'form': form_class}
#     # context = {'form':form_class, 'student':model}
#     # return render(request, 'sis_app/Student_Form_disabled.html', context)

# def editStudentForm(request,id):

@login_required(login_url='sis_app:log_in')
def RegistrationList(request, pk = 0):
    if request.user.is_superuser:
        registrant_ids = list(Student.objects.values_list('pk', flat=True).order_by('pk'))
        user_ids = list(User.objects.exclude(is_superuser=True).values_list('pk', flat=True).order_by('pk'))
        view_registrant_ids = list(set(registrant_ids) - set(user_ids))

        students = Student.objects.filter(pk__in=view_registrant_ids)
        myFilter = StudentFilter(request.GET, queryset=students)
        students = myFilter.qs

        #transfer to GenerateAccount later
        
        context = {'studentList' : students, 'myFilter': myFilter}

        return render(request,"sis_app/Registration_List.html", context)
    else:
        return redirect('sis_app:home')

def username_exists(username):
    return User.objects.filter(username=username).exists()

@login_required(login_url='sis_app:log_in')
def GenerateAccount(request, id):
    # if request.user.is_superuser:
    if request.user.is_superuser:
   
        test = Student.objects.get(pk=id)

        while True:
            user_length = 10
            pass_length = 15
            username = ''.join(random.choices(string.ascii_uppercase + string.digits, k = user_length))
            password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = pass_length))

            if username_exists(username) == False:
                user = User.objects.create_user(id = test.id, username = username, email = test.student_guardianemail, password = password, first_name = str(test.student_firstname), last_name = test.student_lastname)
            
                send_mail(
                    'CAMELEAN ACADEMY SIS username and pass',
                    "Username: {}\nPassword: {}\nPLEASE CHANGE YOUR USERNAME AND PASSWORD UPON FIRST LOG-IN".format(username, password),
                    None,
                    [str(test.student_guardianemail)],#this is the recipient(change this to email of student later)
                    fail_silently=False,
                )

                return redirect("/RegistrationList")
                False
            else:   
                continue

        ##MAKE A SEPARATE PAGE FOR DISPLAYING USERNAME AND PASS OF EACH USER
    else:
            return redirect('sis_app:home')
    # Create your views here.

@login_required(login_url='sis_app:log_in')
def updateEnrollmentStatus(request, id):
    test = Student.objects.get(pk = id)
    if test.enrollment_status == "Not Enrolled":
        test.enrollment_status = "Enrolled"
        test.save()
    elif test.enrollment_status == "Enrolled":
        test.enrollment_status = "Not Enrolled"
        test.save()

@login_required(login_url='sis_app:log_in')
def paymentForm(request, id):
    # model = Payment
    # form_class = PaymentForm
    annual = 37999
    biannual = 38998
    quarterly = 41663 
    if request.method == "GET":
        form = PaymentForm
        return render(request,"sis_app/Payment_Form.html",{'form':form})
    else:
        student = Student.objects.get(pk=id)
        sy_end = student.student_schoolyear_start
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            # payments = Payment.objects.filter(payment_s_account_id = id)
            # sy_end = form.cleaned_data['school_year_end']
            # paymentstudentid = Payment.objects.filter(payment_s_account_id = id).last()
            paymentstudentid = Payment.objects.latest('id')
            paymentstudentid.payment_s_account_id = student
            paymentstudentid.save()
            paymentstudentid.school_year_end = sy_end
            paymentstudentid.save()
            studentID = paymentstudentid.getstudentid()
            studentIDobject = Student.objects.get(pk = studentID)
            enrollment_plan = studentIDobject.student_enrollment_plan
        
            #Subtract payment amount field from the most recent outstanding balance
              
            # school_year_end = paymentstudentid.school_year_end
            # sy_end = form.cleaned_data['school_year_end']
            payments_in_year = Payment.objects.filter(payment_s_account_id = id).filter(school_year_end = sy_end)
            print(payments_in_year)
            print(paymentstudentid.outstandingbalance)
            if paymentstudentid.outstandingbalance == 1000000 and len(payments_in_year)==1:
                if enrollment_plan == "Annually":
                    paymentstudentid.outstandingbalance = annual
                elif enrollment_plan == "Bi-Annually":
                    paymentstudentid.outstandingbalance = biannual
                else:
                    paymentstudentid.outstandingbalance = quarterly
                paymentstudentid.save()
            else:
                o_balance_list = []
                for payment in payments_in_year:
                    o_balance_list.append(payment.outstandingbalance)
                paymentstudentid.outstandingbalance = min(o_balance_list)
                paymentstudentid.save()
            payment_amount = form.cleaned_data['payment_amount']
    
            print(paymentstudentid.outstandingbalance)
            paymentstudentid.outstandingbalance = paymentstudentid.outstandingbalance - payment_amount
    
            paymentstudentid.save()
            print(paymentstudentid.outstandingbalance)

            updateEnrollmentStatus(request, id)
            payments = Payment.objects.latest('id')
            student = Student.objects.get(pk=id)
            payments.enrollment_type = student.student_enrollment_plan
            payments.save()

            return redirect('/paymentList')
        else:
            messages.error(request, 'error')
            # return redirect('sis_app:student_paymentview')
            return redirect(f'/paymentForm/{id}')
        # return HttpResponseRedirect("/paymentForm/{id}".format(id=id))

# def paymentForm(request,id=0):
#     if request.user.is_superuser:
#         model = Payment
#         form_class = PaymentForm
#         if request.method == "GET":
#             if id == 0: 
#                 form = PaymentForm()
#             else:
#                 payment = Payment.objects.get(pk=id)
#                 form = PaymentForm(instance=payment)
#             return render(request,"sis_app/Payment_Form.html",{'form':form})
#         else:
#             #Values for Varying Student Enrollment Plan
#             annual = 37999
#             biannual = 38998
#             quarterly = 41663

#             if id == 0:
#                 form = PaymentForm(request.POST)
#             else:
#                 payment = Payment.objects.get(pk=id)
#                 form = PaymentForm(request.POST,instance=payment)
#             if form.is_valid():
#                 form.save()

#                 s_id = form.cleaned_data['payment_s_account_id']
#                 payments = Payment.objects.filter(payment_s_account_id = s_id)
    
#                 #paymentstudentid = Payment.objects.latest('payment_s_account_id')
#                 sy_end = form.cleaned_data['school_year_end']
#                 paymentstudentid = Payment.objects.filter(payment_s_account_id = s_id).filter(school_year_end = sy_end).last()
#                 studentID = paymentstudentid.getstudentid()
#                 studentIDobject = Student.objects.get(pk = studentID)
#                 enrollment_plan = studentIDobject.student_enrollment_plan
        
#                 #Subtract payment amount field from the most recent outstanding balance
              
#                 school_year_end = paymentstudentid.school_year_end
#                 sy_end = form.cleaned_data['school_year_end']
#                 #print(current_year)
#                 payments_in_year = Payment.objects.filter(payment_s_account_id = s_id).filter(school_year_end = sy_end)
#                 print(payments_in_year)
#                 print(paymentstudentid.outstandingbalance)
#                 if paymentstudentid.outstandingbalance == 1000000 and len(payments_in_year)==1:
#                     if enrollment_plan == "Annually":
#                         paymentstudentid.outstandingbalance = annual
#                     elif enrollment_plan == "Bi-Annually":
#                         paymentstudentid.outstandingbalance = biannual
#                     else:
#                         paymentstudentid.outstandingbalance = quarterly
#                     paymentstudentid.save()
#                 else:
#                     o_balance_list = []
#                     for payment in payments_in_year:
#                         o_balance_list.append(payment.outstandingbalance)
#                     paymentstudentid.outstandingbalance = min(o_balance_list)
#                     paymentstudentid.save()
#                 payment_amount = form.cleaned_data['payment_amount']
        
#                 print(paymentstudentid.outstandingbalance)
#                 paymentstudentid.outstandingbalance = paymentstudentid.outstandingbalance - payment_amount
        
#                 paymentstudentid.save()
#                 print(paymentstudentid.outstandingbalance)

#                 updateEnrollmentStatus(request, s_id.id)

#             return redirect('/paymentList')
#     else:
#             return redirect('sis_app:home')

@login_required(login_url='sis_app:log_in')
def paymentList(request):
    if request.user.is_superuser:
        payments = Payment.objects.all()

        myPFilter = PaymentFilter(request.GET, queryset=payments)
        payments = myPFilter.qs

        #print(payments)

        # Payment.objects.filter(getstudentenrollmentstatus="Not Enrolled").update(getstudentenrollmentstatus = "Enrolled")
        

        context = {'paymentList' : payments, 'myPFilter': myPFilter}
        return render(request,"sis_app/paymentList.html", context)
    else:
        return redirect('sis_app:home')

@login_required(login_url='sis_app:log_in')
def resetBAEnrollmentStatus(request):
    if request.user.is_superuser:
        Student.objects.filter(student_enrollment_plan = "Bi-Annually").update(enrollment_status = "Not Enrolled")
        return redirect('/paymentList')
    else:
        return redirect('sis_app:home')


@login_required(login_url='sis_app:log_in')
def resetQEnrollmentStatus(request):
    if request.user.is_superuser:
        Student.objects.filter(student_enrollment_plan = "Quarterly").update(enrollment_status = "Not Enrolled")
        return redirect('/paymentList')
    else:
        return redirect('sis_app:home')

@login_required(login_url='sis_app:log_in')
def resetALLEnrollmentStatus(request):
    if request.user.is_superuser:
        Student.objects.all().update(enrollment_status = "Not Enrolled")
        return redirect('/paymentList')
    else:
        return redirect('sis_app:log_in')

@login_required(login_url='sis_app:log_in')
def EnrollmentStatusAndPaymentPlan(request):
    if request.user.is_superuser:
        students = Student.objects.all()

        myFilter2 = EnrollmentStatusAndPaymentPlanFilter(request.GET, queryset=students)
        students = myFilter2.qs

        context = {'studentList' : students, 'myFilter2': myFilter2}
        return render(request,"sis_app/Student_Enrollment.html", context)   
    else:
        return redirect('sis_app:home')

@login_required(login_url='sis_app:log_in')
def StudentPaymentView(request):
    user_id = request.user.id
    student = Student.objects.get(pk = user_id)
    # paymentstudentid = Payment.objects.filter(payment_s_account_id = user_id).latest('payment_s_account_id')
    paymentstudentid = Payment.objects.filter(payment_s_account_id = user_id).latest('id')

    student_payments = Payment.objects.filter(payment_s_account_id = user_id)
    sy_start = student.student_schoolyear_start
    sy_end = sy_start + 1
    context = {"student": student, "payment": paymentstudentid, "payments":student_payments, "sy_start": sy_start, "sy_end":sy_end}
    return render(request, "sis_app/Student_PaymentView.html", context)

#GradeReport List for Nursery students only
@login_required(login_url='sis_app:log_in')
def GradeReportList_Nursery(request):
    if request.user.is_superuser:
        students = Student.objects.filter(student_grade_level = 'Nursery')
        student = {'studentList' : students}
        return render(request,"sis_app/GradeReportNursery_List.html", student)
    # students = GradeReport.objects.all()
    # studentgrade = {'GradeReportList' : students}
    # return render(request,"sis_app/GradeReportNursery_List.html", studentgrade)
    else:
        return redirect('sis_app:home')

#GradeReport Form for Nursery students only
def RetrieveAccount(request):
    return None

@login_required(login_url='sis_app:log_in')
def GradeReportFormNursery(request, id):
    if request.user.is_superuser:
        model = GradeReport
        form_class = GradeReportFormN
        student = Student.objects.get(pk=id)
        if request.method == 'POST':
            if TranscriptOfRecord.objects.filter(student = student).exists():
                tor = TranscriptOfRecord.objects.get(student = student)
                form = GradeReportFormN(request.POST)
            else:
                tor = TranscriptOfRecord.objects.create(tor_id=id, student = student)
                form = GradeReportFormN(request.POST)
            if form.is_valid():
                form.save()
                report = GradeReport.objects.latest('id')
                tor_obj = TranscriptOfRecord.objects.get(tor_id=id)
                report.tor_id = tor_obj
                report.student = student
                report.save()

                #Language Grade for Nursery
                language = (report.Nlanguage1, report.Nlanguage2, report.Nlanguage3, report.Nlanguage4, report.Nlanguage5, report.Nlanguage6, report.Nlanguage7, report.Nlanguage8, report.Nlanguage9, report.Nlanguage10)
                languagelist1 = list(language)
                languagelist2 = []
                languagetotal = 0
                for i in languagelist1:
                    if i == 'O':
                        i = 98
                        languagelist2.append(i)
                    elif i == 'VG':
                        i = 93
                        languagelist2.append(i)
                    elif i == 'G':
                        i = 87
                        languagelist2.append(i)
                    elif i == 'F':
                        i = 82
                        languagelist2.append(i)
                    else:
                        languagelist1.remove(i)
                for i in languagelist2:
                    languagetotal += i
                languageaverage =(languagetotal/len(languagelist2))
                report.N_language = languageaverage
                report.save()
                
                #Reading Readiness Grade for Nursery
                readingreadiness = (report.N_reading_readiness1, report.N_reading_readiness2, report.N_reading_readiness3, report.N_reading_readiness4, report.N_reading_readiness5, report.N_reading_readiness6, 
                report.N_reading_readiness7, report.N_reading_readiness8, report.N_reading_readiness9, report.N_reading_readiness10, report.N_reading_readiness11, report.N_reading_readiness12, report.N_reading_readiness13)
                readingreadinesslist1 = list(readingreadiness)
                readingreadinesslist2 = []
                readingreadinesstotal = 0
                for i in readingreadinesslist1:
                    if i == 'O':
                        i = 98
                        readingreadinesslist2.append(i)
                    elif i == 'VG':
                        i = 93
                        readingreadinesslist2.append(i)
                    elif i == 'G':
                        i = 87
                        readingreadinesslist2.append(i)
                    elif i == 'F':
                        i = 82
                        readingreadinesslist2.append(i)
                    else:
                        readingreadinesslist1.remove(i)
                for i in readingreadinesslist2:
                    readingreadinesstotal += i
                readingreadinessaverage =(readingreadinesstotal/len(readingreadinesslist2))
                report.N_reading_readiness = readingreadinessaverage
                report.save()

                #Numbber Readiness Grade for Nursery
                numberreadiness = (report.N_number_readiness1, report.N_number_readiness2, report.N_number_readiness3, report.N_number_readiness4, report.N_number_readiness5, report.N_number_readiness6, 
                report.N_number_readiness7, report.N_number_readiness8)
                numberreadinesslist1 = list(numberreadiness)
                numberreadinesslist2 = []
                numberreadinesstotal = 0
                for i in numberreadinesslist1:
                    if i == 'O':
                        i = 98
                        numberreadinesslist2.append(i)
                    elif i == 'VG':
                        i = 93
                        numberreadinesslist2.append(i)
                    elif i == 'G':
                        i = 87
                        numberreadinesslist2.append(i)
                    elif i == 'F':
                        i = 82
                        numberreadinesslist2.append(i)
                    else:
                        numberreadinesslist1.remove(i)
                for i in numberreadinesslist2:
                    numberreadinesstotal += i
                numberreadinessaverage =(numberreadinesstotal/len(numberreadinesslist2))
                report.N_number_readiness = numberreadinessaverage
                report.save()

                #Science Grade for Nursery
                science = (report.N_science1, report.N_science2, report.N_science3, report.N_science4, report.N_science5, report.N_science6)
                sciencelist1 = list(science)
                sciencelist2 = []
                sciencetotal = 0
                for i in sciencelist1:
                    if i == 'O':
                        i = 98
                        sciencelist2.append(i)
                    elif i == 'VG':
                        i = 93
                        sciencelist2.append(i)
                    elif i == 'G':
                        i = 87
                        sciencelist2.append(i)
                    elif i == 'F':
                        i = 82
                        sciencelist2.append(i)
                    else:
                        sciencelist1.remove(i)
                for i in sciencelist2:
                    sciencetotal += i
                scienceaverage =(sciencetotal/len(sciencelist2))
                report.N_science = scienceaverage
                report.save()

                #Interpersonal Skills Grade for Nursery
                interpersonalskills = (report.N_interpersonal_skills1, report.N_interpersonal_skills2, report.N_interpersonal_skills3, report.N_interpersonal_skills4, 
                report.N_interpersonal_skills5, report.N_interpersonal_skills6, report.N_interpersonal_skills7, report.N_interpersonal_skills8, report.N_interpersonal_skills9, 
                report.N_interpersonal_skills10, report.N_interpersonal_skills11, report.N_interpersonal_skills12, report.N_interpersonal_skills13)
                interpersonalskillslist1 = list(interpersonalskills)
                interpersonalskillslist2 = []
                interpersonalskillstotal = 0
                for i in interpersonalskillslist1:
                    if i == 'O':
                        i = 98
                        interpersonalskillslist2.append(i)
                    elif i == 'VG':
                        i = 93
                        interpersonalskillslist2.append(i)
                    elif i == 'G':
                        i = 87
                        interpersonalskillslist2.append(i)
                    elif i == 'F':
                        i = 82
                        interpersonalskillslist2.append(i)
                    else:
                        interpersonalskillslist1.remove(i)
                for i in interpersonalskillslist2:
                    interpersonalskillstotal += i
                interpersonalskillsaverage =(interpersonalskillstotal/len(interpersonalskillslist2))
                report.N_interpersonal_skills = interpersonalskillsaverage
                report.save()

                #Motor Skills Grade for Nursery
                motorskills = (report.N_motor_skills1, report.N_motor_skills2, report.N_motor_skills3, report.N_motor_skills4, 
                report.N_motor_skills5, report.N_motor_skills6, report.N_motor_skills7, report.N_motor_skills8, report.N_motor_skills9, 
                report.N_motor_skills10, report.N_motor_skills11, report.N_motor_skills12, report.N_motor_skills13)
                motorskillslist1 = list(motorskills)
                motorskillslist2 = []
                motorskillstotal = 0
                for i in motorskillslist1:
                    if i == 'O':
                        i = 98
                        motorskillslist2.append(i)
                    elif i == 'VG':
                        i = 93
                        motorskillslist2.append(i)
                    elif i == 'G':
                        i = 87
                        motorskillslist2.append(i)
                    elif i == 'F':
                        i = 82
                        motorskillslist2.append(i)
                    else:
                        motorskillslist1.remove(i)
                for i in motorskillslist2:
                    motorskillstotal += i
                motorskillsaverage =(motorskillstotal/len(motorskillslist2))
                report.N_motor_skills = motorskillsaverage
                report.save()

                #Creative Domain Grade for Nursery
                creativedomain = (report.N_creative_domain1, report.N_creative_domain2, report.N_creative_domain3, report.N_creative_domain4, 
                report.N_creative_domain5)
                creativedomainlist1 = list(creativedomain)
                creativedomainlist2 = []
                creativedomaintotal = 0
                for i in creativedomainlist1:
                    if i == 'O':
                        i = 98
                        creativedomainlist2.append(i)
                    elif i == 'VG':
                        i = 93
                        creativedomainlist2.append(i)
                    elif i == 'G':
                        i = 87
                        creativedomainlist2.append(i)
                    elif i == 'F':
                        i = 82
                        creativedomainlist2.append(i)
                    else:
                        creativedomainlist1.remove(i)
                for i in creativedomainlist2:
                    creativedomaintotal += i
                creativedomainaverage =(creativedomaintotal/len(creativedomainlist2))
                report.N_creative_domain = creativedomainaverage
                report.save()

                #Good Morals and Value Formation Grade for Nursery
                moralvalueformation = (report.N_good_moral_valueformation1, report.N_good_moral_valueformation2, report.N_good_moral_valueformation3, report.N_good_moral_valueformation4, 
                report.N_good_moral_valueformation5, report.N_good_moral_valueformation6, report.N_good_moral_valueformation7, report.N_good_moral_valueformation8, report.N_good_moral_valueformation9)
                moralvalueformationlist1 = list(moralvalueformation)
                moralvalueformationlist2 = []
                moralvalueformationtotal = 0
                for i in moralvalueformationlist1:
                    if i == 'O':
                        i = 98
                        moralvalueformationlist2.append(i)
                    elif i == 'VG':
                        i = 93
                        moralvalueformationlist2.append(i)
                    elif i == 'G':
                        i = 87
                        moralvalueformationlist2.append(i)
                    elif i == 'F':
                        i = 82
                        moralvalueformationlist2.append(i)
                    else:
                        moralvalueformationlist1.remove(i)
                for i in moralvalueformationlist2:
                    moralvalueformationtotal += i
                moralvalueformationaverage =(moralvalueformationtotal/len(moralvalueformationlist2))
                report.N_good_moral_valueformation = moralvalueformationaverage
                report.save()

                #Sem Average (Average of all academic subject grades)
                semaverage = (report.N_language, report.N_reading_readiness, report.N_number_readiness, report.N_science, report.N_interpersonal_skills, report.N_motor_skills, 
                report.N_creative_domain, report.N_good_moral_valueformation)
                semaveragelist1 = list(semaverage)
                semaveragelist2 = []
                semaveragetotal = 0
                for i in semaveragelist1:
                    if i != None:
                        semaveragelist2.append(i)
                for i in semaveragelist2:
                    semaveragetotal += i
                semaverage1 =(semaveragetotal/len(semaveragelist2))
                report.sem_average = semaverage1
                report.save()

                # Filter objects to specific student 
                x = GradeReport.objects.select_related().filter(student = id)

                #Filter objects to specific student and school year
                sy = form.cleaned_data['school_year']
                filteredsy = x.filter(school_year = sy)

                # (FINAL RATING) Average of all language grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.N_language
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                if yearaverage >= 96 and yearaverage <= 100:
                    yearaverage = 'O'
                elif yearaverage >= 90 and yearaverage <= 95:
                    yearaverage = 'VG'
                elif yearaverage >= 85 and yearaverage <= 89:
                    yearaverage = 'G'
                else:
                    yearaverage = 'F'

                report.N_final_language = yearaverage
                report.save()

                # (FINAL RATING) Average of all Reading Readiness grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.N_reading_readiness
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                if yearaverage >= 96 and yearaverage <= 100:
                    yearaverage = 'O'
                elif yearaverage >= 90 and yearaverage <= 95:
                    yearaverage = 'VG'
                elif yearaverage >= 85 and yearaverage <= 89:
                    yearaverage = 'G'
                else:
                    yearaverage = 'F'

                report.N_final_reading_readiness = yearaverage
                report.save()


                # (FINAL RATING) Average of all number readiness grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.N_number_readiness
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                if yearaverage >= 96 and yearaverage <= 100:
                    yearaverage = 'O'
                elif yearaverage >= 90 and yearaverage <= 95:
                    yearaverage = 'VG'
                elif yearaverage >= 85 and yearaverage <= 89:
                    yearaverage = 'G'
                else:
                    yearaverage = 'F'

                report.N_final_number_readiness = yearaverage
                report.save()

                # (FINAL RATING) Average of all science grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.N_science
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                if yearaverage >= 96 and yearaverage <= 100:
                    yearaverage = 'O'
                elif yearaverage >= 90 and yearaverage <= 95:
                    yearaverage = 'VG'
                elif yearaverage >= 85 and yearaverage <= 89:
                    yearaverage = 'G'
                else:
                    yearaverage = 'F'

                report.N_final_science = yearaverage
                report.save()


                # (FINAL RATING) Average of all interpersonal grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.N_interpersonal_skills
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                if yearaverage >= 96 and yearaverage <= 100:
                    yearaverage = 'O'
                elif yearaverage >= 90 and yearaverage <= 95:
                    yearaverage = 'VG'
                elif yearaverage >= 85 and yearaverage <= 89:
                    yearaverage = 'G'
                else:
                    yearaverage = 'F'

                report.N_final_interpersonal_skills = yearaverage
                report.save()

                # (FINAL RATING) Average of all motor skills grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.N_motor_skills
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                if yearaverage >= 96 and yearaverage <= 100:
                    yearaverage = 'O'
                elif yearaverage >= 90 and yearaverage <= 95:
                    yearaverage = 'VG'
                elif yearaverage >= 85 and yearaverage <= 89:
                    yearaverage = 'G'
                else:
                    yearaverage = 'F'

                report.N_final_motor_skills = yearaverage
                report.save()

                # (FINAL RATING) Average of all creative domain grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.N_creative_domain
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                if yearaverage >= 96 and yearaverage <= 100:
                    yearaverage = 'O'
                elif yearaverage >= 90 and yearaverage <= 95:
                    yearaverage = 'VG'
                elif yearaverage >= 85 and yearaverage <= 89:
                    yearaverage = 'G'
                else:
                    yearaverage = 'F'

                report.N_final_creative_domain = yearaverage
                report.save()

                # (FINAL RATING) Average of all good morals and value formation grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.N_good_moral_valueformation
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                if yearaverage >= 96 and yearaverage <= 100:
                    yearaverage = 'O'
                elif yearaverage >= 90 and yearaverage <= 95:
                    yearaverage = 'VG'
                elif yearaverage >= 85 and yearaverage <= 89:
                    yearaverage = 'G'
                else:
                    yearaverage = 'F'

                report.N_final_good_moral_valueformation = yearaverage
                report.save()


                # Filter objects to specific student 
                x = GradeReport.objects.select_related().filter(student = id)

                #Filter objects to specific student and school year
                sy = form.cleaned_data['school_year']
                filteredsy = x.filter(school_year = sy)
                filteredperiod = form.cleaned_data['grading_period']

                # (FINAL RATING) Average of all of a student's grades per school year
                
                
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.sem_average
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter

                report.N_year_average = yearaverage
                report.save()


                if filteredperiod == '3':
                    if yearaverage >= 96 and yearaverage <= 100:
                        yearaverage = 'O'
                    elif yearaverage >= 90 and yearaverage <= 95:
                        yearaverage = 'VG'
                    elif yearaverage >= 85 and yearaverage <= 89:
                        yearaverage = 'G'
                    else:
                        yearaverage = 'F'
                    
                    report.N_year_average = yearaverage
                    report.save()
                report.gradelevel = student.student_grade_level
                report.save()
                return redirect('sis_app:grade_report_nursery')
            else:
                messages.error(request, 'error')
        context = {'form':form_class}
        return render(request, 'sis_app/GradeReportForm_Nursery.html', context)
    else:
        return redirect('sis_app:home')

#GradeReport List for Kinder 1 and Kinder 2 Junior students only
@login_required(login_url='sis_app:log_in')
def GradeReportList_Kinder1Kinder2Junior(request):
    if request.user.is_superuser:
        students = Student.objects.filter(student_grade_level__in = ['Kinder 1', 'Kinder 2 Junior'])
        student = {'studentList' : students}
        return render(request,"sis_app/GradeReportK1K2JR_List.html", student)
    else:
        return redirect('sis_app:home')

#GradeReport Form for Kinder 1 and Kinder 2 Junior students only
@login_required(login_url='sis_app:log_in')
def GradeReportFormKinder1Kinder2Junior(request, id):
    if request.user.is_superuser:
        model = GradeReport
        form_class = GradeReportFormK1K2JR
        student = Student.objects.get(pk=id)
        if request.method == 'POST':
            if TranscriptOfRecord.objects.filter(student = student).exists():
                tor = TranscriptOfRecord.objects.get(student = student)
                form = GradeReportForm(request.POST)
            else:
                tor = TranscriptOfRecord.objects.create(tor_id=id, student = student)
                form = GradeReportForm(request.POST)
            if form.is_valid():
                form.save()
                report = GradeReport.objects.latest('id')
                tor_obj = TranscriptOfRecord.objects.get(tor_id=id)
                report.tor_id = tor_obj
                report.student = student
                report.save()
                
                #FOR AVERAGES: FIX ERROR (zero over zero) when one subject has no value at all
                #Reading Readiness Grade
                readingreadiness = (report.readingreadiness1, report.readingreadiness2, report.readingreadiness3, report.readingreadiness4, report.readingreadiness5, report.readingreadiness6,
                report.readingreadiness7, report.readingreadiness8, report.readingreadiness9, report.readingreadiness10, report.readingreadiness11, report.readingreadiness12, report.readingreadiness13)
                readingreadinesslist1 = list(readingreadiness)
                readingreadinesslist2 = []
                readingtotal = 0
                for i in readingreadinesslist1:
                    if i != None:
                        readingreadinesslist2.append(i)
                for i in readingreadinesslist2:
                    readingtotal += i
                readingreadinessaverage =(readingtotal/len(readingreadinesslist2))
                report.reading_grade = readingreadinessaverage

                print(readingtotal)
                print(len(readingreadinesslist2))

                report.save()


                #Science Readiness Grade
                sciencereadiness = (report.science1, report.science2, report.science3, report.science4, report.science5, report.science6)
                sciencereadinesslist1 = list(sciencereadiness)
                sciencereadinesslist2 = []
                sciencetotal = 0
                for i in sciencereadinesslist1:
                    if i != None:
                        sciencereadinesslist2.append(i)
                for i in sciencereadinesslist2:
                    sciencetotal += i
                sciencereadinessaverage =(sciencetotal/len(sciencereadinesslist2))
                report.science_grade = sciencereadinessaverage
                report.save()


                #Language Readiness Grade
                languagereadiness = (report.language1, report.language2, report.language3, report.language4, report.language5, report.language6, report.language7, 
                report.language8, report.language9, report.language10)
                languagereadinesslist1 = list(languagereadiness)
                languagereadinesslist2 = []
                languagetotal = 0
                for i in languagereadinesslist1:
                    if i != None:
                        languagereadinesslist2.append(i)
                for i in languagereadinesslist2:
                    languagetotal += i
                languagereadinessaverage =(languagetotal/len(languagereadinesslist2))
                report.language_grade = languagereadinessaverage
                report.save()

                #Mathematics Readiness Grade
                mathreadiness = (report.math1, report.math2, report.math3, report.math4, report.math5, report.math6, report.math7, report.math8,
                report.math9, report.math10, report.math11)
                mathreadinesslist1 = list(mathreadiness)
                mathreadinesslist2 = []
                mathtotal = 0
                for i in mathreadinesslist1:
                    if i != None:
                        mathreadinesslist2.append(i)
                for i in mathreadinesslist2:
                    mathtotal += i
                mathreadinessaverage =(mathtotal/len(mathreadinesslist2))
                report.mathematics_grade = mathreadinessaverage
                report.save()

                #Penmanship Readiness Grade
                penmanshipreadiness = (report.penmanship1, report.penmanship2, report.penmanship3, report.penmanship4)
                penmanshipreadinesslist1 = list(penmanshipreadiness)
                penmanshipreadinesslist2 = []
                penmanshiptotal = 0
                for i in penmanshipreadinesslist1:
                    if i != None:
                        penmanshipreadinesslist2.append(i)
                for i in penmanshipreadinesslist2:
                    penmanshiptotal += i
                penmanshipreadinessaverage =(penmanshiptotal/len(penmanshipreadinesslist2))
                report.penmanship_grade = penmanshipreadinessaverage
                report.save()

                #Sem Average (Average of all academic subject grades)
                semaverage = (report.reading_grade, report.mathematics_grade, report.language_grade, report.science_grade, report.penmanship_grade)
                semaveragelist1 = list(semaverage)
                semaveragelist2 = []
                semaveragetotal = 0
                for i in semaveragelist1:
                    if i != None:
                        semaveragelist2.append(i)
                for i in semaveragelist2:
                    semaveragetotal += i
                semaverage1 =(semaveragetotal/len(semaveragelist2))
                report.sem_average = semaverage1
                report.save()

                # Filter objects to specific student 
                x = GradeReport.objects.select_related().filter(student = id)

                #Filter objects to specific student and school year
                sy = form.cleaned_data['school_year']
                filteredsy = x.filter(school_year = sy)

                # (FINAL RATING) Average of all reading grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.reading_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_reading = yearaverage
                report.save()

                # (FINAL RATING) Average of all mathematics grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.mathematics_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_mathematics = yearaverage
                report.save()

                # (FINAL RATING) Average of all language grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.language_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_language = yearaverage
                report.save()

                # (FINAL RATING) Average of all science grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.science_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_science = yearaverage
                report.save()

                # (FINAL RATING) Average of all penmanship grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.penmanship_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_penmanship = yearaverage
                report.save()

                # (FINAL RATING) Average of all of a student's grades per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.sem_average
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.year_average = yearaverage
                report.save()
                report.gradelevel = student.student_grade_level
                report.save()

                return redirect('sis_app:grade_report_k1k2jr')
            else:
                messages.error(request, 'error')
        context = {'form':form_class}
        return render(request, 'sis_app/GradeReportForm_K1K2JR.html', context)
    else:
        return redirect('sis_app:home')



#GradeReport List for Kinder 2 Senior students only
@login_required(login_url='sis_app:log_in')
def GradeReportList_Kinder2Senior(request):
    if request.user.is_superuser:
        students = Student.objects.filter(student_grade_level = 'Kinder 2 Senior')
        student = {'studentList' : students}
        return render(request,"sis_app/GradeReportKinder2Senior_List.html", student)
    else:
        return redirect('sis_app:home')

#GradeReport Form for Kinder 2 Senior students only
@login_required(login_url='sis_app:log_in')
def GradeReportFormKinder2Senior(request, id):
    if request.user.is_superuser:
        model = GradeReport
        form_class = GradeReportFormK2SR
        student = Student.objects.get(pk=id)
        if request.method == 'POST':
            if TranscriptOfRecord.objects.filter(student = student).exists():
                tor = TranscriptOfRecord.objects.get(student = student)
                form = GradeReportForm(request.POST)
            else:
                tor = TranscriptOfRecord.objects.create(tor_id=id, student = student)
                form = GradeReportForm(request.POST)
            if form.is_valid():
                form.save()
                report = GradeReport.objects.latest('id')
                tor_obj = TranscriptOfRecord.objects.get(tor_id=id)
                report.tor_id = tor_obj
                report.student = student
                report.save()
                
                #FOR AVERAGES: FIX ERROR (zero over zero) when one subject has no value at all
                #Reading Readiness Grade
                readingreadiness = (report.readingreadiness1, report.readingreadiness2, report.readingreadiness3, report.readingreadiness4, report.readingreadiness5, report.readingreadiness6,
                report.readingreadiness7, report.readingreadiness8, report.readingreadiness9, report.readingreadiness10, report.readingreadiness11, report.readingreadiness12, report.readingreadiness13)
                readingreadinesslist1 = list(readingreadiness)
                readingreadinesslist2 = []
                readingtotal = 0
                for i in readingreadinesslist1:
                    if i != None:
                        readingreadinesslist2.append(i)
                for i in readingreadinesslist2:
                    readingtotal += i
                readingreadinessaverage =(readingtotal/len(readingreadinesslist2))
                report.reading_grade = readingreadinessaverage
                report.save()


                #Science Readiness Grade
                sciencereadiness = (report.science1, report.science2, report.science3, report.science4, report.science5, report.science6)
                sciencereadinesslist1 = list(sciencereadiness)
                sciencereadinesslist2 = []
                sciencetotal = 0
                for i in sciencereadinesslist1:
                    if i != None:
                        sciencereadinesslist2.append(i)
                for i in sciencereadinesslist2:
                    sciencetotal += i
                sciencereadinessaverage =(sciencetotal/len(sciencereadinesslist2))
                report.science_grade = sciencereadinessaverage
                report.save()


                #Language Readiness Grade
                languagereadiness = (report.language1, report.language2, report.language3, report.language4, report.language5, report.language6, report.language7, 
                report.language8, report.language9, report.language10)
                languagereadinesslist1 = list(languagereadiness)
                languagereadinesslist2 = []
                languagetotal = 0
                for i in languagereadinesslist1:
                    if i != None:
                        languagereadinesslist2.append(i)
                for i in languagereadinesslist2:
                    languagetotal += i
                languagereadinessaverage =(languagetotal/len(languagereadinesslist2))
                report.language_grade = languagereadinessaverage
                report.save()

                #Mathematics Readiness Grade
                mathreadiness = (report.math1, report.math2, report.math3, report.math4, report.math5, report.math6, report.math7, report.math8,
                report.math9, report.math10, report.math11)
                mathreadinesslist1 = list(mathreadiness)
                mathreadinesslist2 = []
                mathtotal = 0
                for i in mathreadinesslist1:
                    if i != None:
                        mathreadinesslist2.append(i)
                for i in mathreadinesslist2:
                    mathtotal += i
                mathreadinessaverage =(mathtotal/len(mathreadinesslist2))
                report.mathematics_grade = mathreadinessaverage
                report.save()

                #Penmanship Readiness Grade
                penmanshipreadiness = (report.penmanship1, report.penmanship2, report.penmanship3, report.penmanship4)
                penmanshipreadinesslist1 = list(penmanshipreadiness)
                penmanshipreadinesslist2 = []
                penmanshiptotal = 0
                for i in penmanshipreadinesslist1:
                    if i != None:
                        penmanshipreadinesslist2.append(i)
                for i in penmanshipreadinesslist2:
                    penmanshiptotal += i
                penmanshipreadinessaverage =(penmanshiptotal/len(penmanshipreadinesslist2))
                report.penmanship_grade = penmanshipreadinessaverage
                report.save()

                #Filipino Readiness Grade
                filipinoreadiness = (report.filipino1, report.filipino2, report.filipino3, report.filipino4)
                filipinoreadinesslist1 = list(filipinoreadiness)
                filipinoreadinesslist2 = []
                filipinototal = 0
                for i in filipinoreadinesslist1:
                    if i != None:
                        filipinoreadinesslist2.append(i)
                for i in filipinoreadinesslist2:
                    filipinototal += i
                filipinoreadinessaverage =(filipinototal/len(filipinoreadinesslist2))
                report.filipino_grade = filipinoreadinessaverage
                report.save()

                #Sem Average (Average of all academic subject grades)
                semaverage = (report.reading_grade, report.mathematics_grade, report.language_grade, report.science_grade, report.penmanship_grade, report.filipino_grade)
                semaveragelist1 = list(semaverage)
                semaveragelist2 = []
                semaveragetotal = 0
                for i in semaveragelist1:
                    if i != None:
                        semaveragelist2.append(i)
                for i in semaveragelist2:
                    semaveragetotal += i
                semaverage1 =(semaveragetotal/len(semaveragelist2))
                report.sem_average = semaverage1
                report.save()

                # Filter objects to specific student 
                x = GradeReport.objects.select_related().filter(student = id)

                #Filter objects to specific student and school year
                sy = form.cleaned_data['school_year']
                filteredsy = x.filter(school_year = sy)

                # (FINAL RATING) Average of all reading grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.reading_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_reading = yearaverage
                report.save()

                # (FINAL RATING) Average of all mathematics grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.mathematics_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_mathematics = yearaverage
                report.save()

                # (FINAL RATING) Average of all language grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.language_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_language = yearaverage
                report.save()

                # (FINAL RATING) Average of all science grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.science_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_science = yearaverage
                report.save()

                # (FINAL RATING) Average of all penmanship grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.penmanship_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_penmanship = yearaverage
                report.save()

                # (FINAL RATING) Average of all filipino grade per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.filipino_grade
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.final_filipino = yearaverage
                report.save()

                # (FINAL RATING) Average of all of a student's grades per school year
                averagecounter = 0
                average = 0
                for i in filteredsy:
                    average += i.sem_average
                    averagecounter += 1
                else:
                    yearaverage = average/averagecounter
                
                report.year_average = yearaverage
                report.save()
                report.gradelevel = student.student_grade_level
                report.save()

                return redirect('sis_app:grade_report_kinder2senior')
            else:
                messages.error(request, 'error')
        context = {'form':form_class}
        return render(request, 'sis_app/GradeReportForm_Kinder2Senior.html', context)
    else:
        return redirect('sis_app:home')

@login_required(login_url='sis_app:log_in')
def viewGradeReport(request):
    user_id = request.user.id
    student_instance = Student.objects.get(pk = user_id)
    grade_report = GradeReport.objects.filter(student = student_instance).latest('pk')
    model = GradeReport
    form_class = AcknowledgementForm
    if request.method == 'POST':
        x = request.POST.get('gr_acknowledgement')
        if x == 'on':
            x = 'True'
        else:
            x = 'False'
        print(x)
        grade_report.gr_acknowledgement = x
        grade_report.save()
        print(grade_report.gr_acknowledgement)
        return redirect('sis_app:home')  
    print(grade_report)
    context = {"grade_report":grade_report, 'form':form_class}
    if student_instance.student_grade_level == "Nursery":
        return render(request, "sis_app/ViewGradeReportN.html", context)
    elif student_instance.student_grade_level == "Kinder 1" or student_instance.student_grade_level == "Kinder 2 Junior":
        return render(request, "sis_app/ViewGradeReportK1K2JR.html", context)
    elif student_instance.student_grade_level == "Kinder 2 Senior":
        return render(request, "sis_app/ViewGradeReportK2SR.html", context)

    

#make another generateTable functions here to cater to the different grade levels
def generateTable(object):
    object_student = object.student
    student_id = object_student.id
    student_entity = Student.objects.get(pk = student_id)

    #building the table structure
    #Table for Nursery
    if object.gradelevel == 'Nursery':
        gradeTableWidth = 250


        titleTable = Table([
            ['School Year:',  "", object.school_year]
        ],[50, 100, 100])

        
        yearlevelTable = Table([
            ['Year Level:', "", object.gradelevel]
        ],[50,100, 100])

        finalgradeTable = Table([
            ["Reading Readiness", "", object.N_final_reading_readiness],
            ["Math Readiness", "", object.N_final_number_readiness],
            ["Language",  "",object.N_final_language],
            ["Science", "", object.N_final_science],
            ["Interpersonal Skills", "", object.N_final_interpersonal_skills],
            ["Motor Skills", "", object.N_final_motor_skills],
            ["Creative Domain", "", object.N_final_creative_domain],
            ["Year Average", "", object.N_year_average]
        ], [50, 100, 100])

        finalgradeTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('FONTSIZE', (0,0), (-1, -1),10),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
        finalgradeTable.setStyle(finalgradeTableStyle)

        gradeTable = Table([
            [titleTable],
            [yearlevelTable],
            [finalgradeTable]
        ],gradeTableWidth)

        titleTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),10),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
        titleTable.setStyle(titleTableStyle)

        return gradeTable
    #Table for Kinder 1 
    elif object.gradelevel == 'Kinder 1':
        gradeTableWidth = 250


        titleTable = Table([
            ['School Year:',  "", object.school_year]
        ],[50, 100, 100])

        
        yearlevelTable = Table([
            ['Year Level:', "", object.gradelevel]
        ],[50,100, 100])

        finalgradeTable = Table([
            ["Reading", "", object.final_reading],
            ["Math", "", object.final_mathematics],
            ["Language",  "",object.final_language],
            ["Science", "", object.final_science],
            ["Penmanship", "", object.final_penmanship],
        ], [50, 100, 100])

        finalgradeTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('FONTSIZE', (0,0), (-1, -1),10),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
        finalgradeTable.setStyle(finalgradeTableStyle)

        gradeTable = Table([
            [titleTable],
            [yearlevelTable],
            [finalgradeTable]
        ],gradeTableWidth)

        titleTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),10),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
        titleTable.setStyle(titleTableStyle)

        return gradeTable

    #Table for Kinder 2 Junior
    elif object.gradelevel == 'Kinder 2 Junior':
        gradeTableWidth = 250


        titleTable = Table([
            ['School Year:',  "", object.school_year]
        ],[50, 100, 100])

        
        yearlevelTable = Table([
            ['Year Level:', "", object.gradelevel]
        ],[50,100, 100])

        finalgradeTable = Table([
            ["Reading", "", object.final_reading],
            ["Math", "", object.final_mathematics],
            ["Language",  "",object.final_language],
            ["Science", "", object.final_science],
            ["Penmanship", "", object.final_penmanship],
        ], [50, 100, 100])

        finalgradeTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('FONTSIZE', (0,0), (-1, -1),10),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
        finalgradeTable.setStyle(finalgradeTableStyle)

        gradeTable = Table([
            [titleTable],
            [yearlevelTable],
            [finalgradeTable]
        ],gradeTableWidth)

        titleTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),10),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
        titleTable.setStyle(titleTableStyle)

        return gradeTable

    #Table for Kinder 2 Senior
    elif object.gradelevel == 'Kinder 2 Senior':
        gradeTableWidth = 250


        titleTable = Table([
            ['School Year:',  "", object.school_year]
        ],[50, 100, 100])

        
        yearlevelTable = Table([
            ['Year Level:', "", object.gradelevel]
        ],[50,100, 100])

        finalgradeTable = Table([
            ["Reading", "", object.final_reading],
            ["Math", "", object.final_mathematics],
            ["Language",  "",object.final_language],
            ["Science", "", object.final_science],
            ["Penmanship", "", object.final_penmanship],
            ["Filipino", "", object.final_filipino]
        ], [50, 100, 100])

        finalgradeTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('FONTSIZE', (0,0), (-1, -1),10),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
        finalgradeTable.setStyle(finalgradeTableStyle)

        gradeTable = Table([
            [titleTable],
            [yearlevelTable],
            [finalgradeTable]
        ],gradeTableWidth)

        titleTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),10),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
        titleTable.setStyle(titleTableStyle)

        return gradeTable

def generateHeader (student):

    headerTableWidth = 250
    schoolNameTable = Table([
        ['Camelean Academy']
    ],headerTableWidth)

    schoolNameTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),25),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
    schoolNameTable.setStyle(schoolNameTableStyle)

    addressTable = Table([
        ['10 J. Ocampo St. 1109 Quezon City, Philippines']
    ],headerTableWidth)

    adressTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),14),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
    addressTable.setStyle(adressTableStyle)

    docLabelTable = Table([
        ['OFFICIAL TRANSCRIPT OF RECORDS']
    ],headerTableWidth)

    docLabelTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),18),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
    docLabelTable.setStyle(docLabelTableStyle)

    studentLabelTable = Table([
        ['Student: %s' % str(student.student_firstname + ' '+ student.student_lastname), 'Address: %s' % str(student.student_address), 'Birthdate: %s' % str(student.student_birthday)],
    ],[100,100,50])

    studentLabelTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),8),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
    studentLabelTable.setStyle(studentLabelTableStyle)

    headerTable = Table([
        [schoolNameTable],
        [addressTable],
        [docLabelTable],
        [studentLabelTable]
    ], headerTableWidth)

    headerTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ])
    headerTable.setStyle(headerTableStyle)

    return headerTable

def generateFooter(student):
    footerTableWidth = 250

    signatureTable = Table([
        ['____________________',''],
        ['Michael Ross P. Atienza',''],
        ['Camelean Academy School Administrator','']
    ],footerTableWidth)

    signatureTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),10),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
    signatureTable.setStyle(signatureTableStyle)

    studentNameDateTable = Table([
        ['Date Generated: %s' % str(date.today())]
    ],footerTableWidth)

    studentNameDateTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),8),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
    studentNameDateTable.setStyle(studentNameDateTableStyle)

    docLabelTable = Table([
        ['THIS IS AN OFFICIAL ELECTRONIC DOCUMENT ISSUED BY CAMELEAN ACADEMY.']
    ],footerTableWidth)

    docLabelTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),7),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
    docLabelTable.setStyle(docLabelTableStyle)

    telNumberTable = Table([
        ['Tel/Fax + 63 2 8421 2595'],
    ],footerTableWidth)

    telNumberTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1, -1),5),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
    telNumberTable.setStyle(telNumberTableStyle)

    footerTable = Table([
        [signatureTable,''],
        [studentNameDateTable],
        [docLabelTable],
        [telNumberTable]
    ], [50,200])

    footerTableStyle = TableStyle([
            ('VALIGN',(0,0),(-1,-1), "BOTTOM")
        ])
    footerTable.setStyle(footerTableStyle)

    return footerTable

def generateGradesTable(grade_list):
    len_report = len(grade_list)
    if len_report == 1:
       p0 = generateTable(grade_list[0])
       gradesTableWidth = 250
       gradesTable = Table([
           [p0]
       ],gradesTableWidth)
       gradesTableStyle = TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (-1, -1),8),
            ('FONTNAME', (0,0), (-1,-1),'Times-Roman')
        ])
        
        
@login_required(login_url='sis_app:log_in')
def generateTOR (request, id):
    if request.user.is_superuser:
        buff = io.BytesIO()
        # response = HttpResponse(content_type='application/pdf')
        grade_report = GradeReport.objects.filter(student__pk = id, grading_period = '3')
        if len(grade_report) == 0:
            messages.error(request, 'error')
            return redirect(f'/studentList')
        else:
            object0 = grade_report[0]
            object_student = object0.student
            student_id = object_student.id
            student_entity = Student.objects.get(pk = student_id)
            pdf_name = "Transcript of Records-%s.pdf" % str(student_entity.student_lastname)
            
            tor_pdf = SimpleDocTemplate(buff, pagesize = letter, topMargin = 0.1)
            
            if len(grade_report) == 0:
                messages.error(request, 'error')
                return redirect(f'/studentList')
            if len(grade_report) == 1:
                p0 = generateTable(grade_report[0])
                o1 = generateHeader(student_entity)
                f1 = generateFooter(student_entity)
                
                #start of making bigTable
                bigTableWidth = 250

                headerTable = Table([
                    [o1]
                ],bigTableWidth)
                headerTableStyle = TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ])
                headerTable.setStyle(headerTableStyle)

                gradesTable = Table([
                    [p0,'','']
                ],bigTableWidth)
                gradesTableStyle = TableStyle([
                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0,0), (-1, -1),8),
                    ('FONTNAME', (0,0), (-1,-1),'Times-Roman'),
                    ('VALIGN',(0,0),(-1,-1), "TOP")
                ])
                gradesTable.setStyle(gradesTableStyle)

                footerTable = Table([
                    [f1]
                ],bigTableWidth)
                footerTableStyle = TableStyle([
                    ('VALIGN',(0,0),(-1,-1), "BOTTOM"),
                    ('TOPPADDING',(0,0),(-1,-1), 296)#change this value
                ])
                footerTable.setStyle(footerTableStyle)


                bigTable = Table([
                    [headerTable],
                    [gradesTable],
                    [footerTable]
                ],bigTableWidth)

                #end of making bigTable
                elems = []    
                elems.append(bigTable)
                print(grade_report)
                tor_pdf.build(elems)
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
                response.write(buff.getvalue())
                buff.close()    
                return response
            elif len(grade_report) == 2:
                p0 = generateTable(grade_report[0])
                p1 = generateTable(grade_report[1])
                o1 = generateHeader(student_entity)
                f1 = generateFooter(student_entity)

                #start of making bigTable
                bigTableWidth = 250

                headerTable = Table([
                    [o1]
                ],bigTableWidth)
                headerTableStyle = TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ])
                headerTable.setStyle(headerTableStyle)

                gradesTable = Table([
                    [p0,'',p1]
                ],[5,240,5])
                gradesTableStyle = TableStyle([
                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0,0), (-1, -1),8),
                    ('FONTNAME', (0,0), (-1,-1),'Times-Roman'),
                    ('VALIGN',(0,0),(-1,-1), "TOP")
                ])
                gradesTable.setStyle(gradesTableStyle)

                footerTable = Table([
                    [f1]
                ],bigTableWidth)
                footerTableStyle = TableStyle([
                    ('VALIGN',(0,0),(-1,-1), "BOTTOM"),
                    ('TOPPADDING',(0,0),(-1,-1), 296)#change this value
                ])
                footerTable.setStyle(footerTableStyle)

                bigTable = Table([
                    [headerTable],
                    [gradesTable],
                    [footerTable]
                ],bigTableWidth)

                #end of making bigTable

                elems = []    
                elems.append(bigTable)
                print(grade_report)
                tor_pdf.build(elems)
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
                response.write(buff.getvalue())
                buff.close()   
                return response
            elif len(grade_report) == 3:
                p0 = generateTable(grade_report[0])
                p1 = generateTable(grade_report[1])
                p2 = generateTable(grade_report[2])
                o1 = generateHeader(student_entity)
                f1 = generateFooter(student_entity)
                #start of making bigTable
                bigTableWidth = 250

                headerTable = Table([
                    [o1]
                ],bigTableWidth)
                headerTableStyle = TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ])
                headerTable.setStyle(headerTableStyle)

                gradesTable = Table([
                    [p0,'',p1],
                    ['',p2,'']
                ],[5,240,5])
                gradesTableStyle = TableStyle([
                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0,0), (-1, -1),8),
                    ('FONTNAME', (0,0), (-1,-1),'Times-Roman'),
                    ('VALIGN',(0,0),(-1,-1), "TOP")
                ])
                gradesTable.setStyle(gradesTableStyle)

                footerTable = Table([
                    [f1]
                ],bigTableWidth)
                footerTableStyle = TableStyle([
                    ('VALIGN',(0,0),(-1,-1), "BOTTOM"),
                    ('TOPPADDING',(0,0),(-1,-1), 150)#change this value
                ])
                footerTable.setStyle(footerTableStyle)


                bigTable = Table([
                    [headerTable],
                    [],
                    [gradesTable],
                    [footerTable]
                ],bigTableWidth)

                #end of making bigTable
                elems = []    
                elems.append(bigTable)
                print(grade_report)
                tor_pdf.build(elems)
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
                response.write(buff.getvalue())
                buff.close()   
                return response
            elif len(grade_report) == 4:
                p0 = generateTable(grade_report[0])
                p1 = generateTable(grade_report[1])
                p2 = generateTable(grade_report[2])
                p3 = generateTable(grade_report[3])
                o1 = generateHeader(student_entity)
                f1 = generateFooter(student_entity)


                #start of making bigTable
                bigTableWidth = 250

                headerTable = Table([
                    [o1]
                ],bigTableWidth)
                headerTableStyle = TableStyle([
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ])
                headerTable.setStyle(headerTableStyle)

                gradesTable = Table([
                    [p0,'',p1],
                    [p2,'',p3]
                ],[5,240,5])
                gradesTableStyle = TableStyle([
                    ('ALIGN', (0,0), (-1, -1), 'CENTER'),
                    ('FONTSIZE', (0,0), (-1, -1),8),
                    ('FONTNAME', (0,0), (-1,-1),'Times-Roman'),
                    ('VALIGN',(0,0),(-1,-1), "TOP")
                ])
                gradesTable.setStyle(gradesTableStyle)

                footerTable = Table([
                    [f1]
                ],bigTableWidth)
                footerTableStyle = TableStyle([
                    ('VALIGN',(0,0),(-1,-1), "BOTTOM"),
                    ('TOPPADDING',(0,0),(-1,-1), 150)#change this value
                ])
                footerTable.setStyle(footerTableStyle)


                bigTable = Table([
                    [headerTable],
                    [gradesTable],
                    [footerTable]
                ],bigTableWidth)

                bigTableStyle = TableStyle([
                    ('TOPPADDING',(0,0),(-1,-1), 0),
                    ('BOTTOMPADDING',(0,0),(-1,-1), 0),
                ])
                bigTable.setStyle(bigTableStyle)

                #end of making bigTable
                elems = []    
                elems.append(bigTable)
                print(grade_report)
                tor_pdf.build(elems)
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
                response.write(buff.getvalue())
                buff.close()   
                return response
    else:
        return redirect('sis_app:home')

@login_required(login_url='sis_app:log_in')
def deleteStudentsPage(request):
    if request.user.is_superuser:
        current_year = date.today().year
        year_to_delete = current_year - 6

        students = Student.objects.filter(student_schoolyear_start = year_to_delete)
        

        context = {'studentList' : students, "year_to_delete":year_to_delete}
        return render(request,"sis_app/Delete_Button.html", context)   
    else:
        return redirect('sis_app:home')
    
@login_required(login_url='sis_app:log_in')
def deleteStudents(request):
    if request.user.is_superuser:
        current_year = date.today().year
        year_to_delete = current_year - 6
        students_to_delete = Student.objects.filter(student_schoolyear_start = year_to_delete)
        print(year_to_delete)
        print(students_to_delete)
        students_to_delete.delete()
        return redirect('/studentList')
    else:
        return redirect('sis_app:home')


@login_required(login_url='sis_app:log_in')
def logout(request):
    django_logout(request)
    return redirect('/login')
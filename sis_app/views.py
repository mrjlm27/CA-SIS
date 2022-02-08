from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
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

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# def hello_world(request):
#     return render(request, 'sis_app/hello_world.html')
def Home(request):
    context={}
    return render(request,'sis_app/home.html',context) 


def LogInScreen(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username = username, password = password)
        if user is not None: #If log-in credentials are correct
            login(request, user)
            return redirect('/home')
    context = {}
    return render(request, 'sis_app/LogIn.html', context)

def EditAccountCred(request):
    # user = User.objects.get(username=request.username, password=request.password)
    # if request.user.is_authenticated():
    if request.method == 'POST':
        old_u = request.user.username
        old_p = request.user.password
        user = User.objects.get(username=old_u,password=old_p)
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        # user.set_username(new_username)
        user.username = new_username
        user.set_password(new_password)
        user.save()
        return redirect('sis_app:log_in')
    context={}
    return render(request, 'sis_app/Account_Edit.html', context)



def StudentList(request):
    students = Student.objects.all()

    myFilter = StudentFilter(request.GET, queryset=students)
    students = myFilter.qs


    context = {'studentList' : students, 'myFilter': myFilter}
    return render(request,"sis_app/Student_List.html", context)

def studentForm(request,id=0):
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
        return redirect('sis_app:log_in')
    context = {'form':form_class}
    return render(request, 'sis_app/Student_Form.html', context)

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
        return render(request,"sis_app/no_access.html")


def username_exists(username):
    return User.objects.filter(username=username).exists()

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
                user = User.objects.create_user(id = test.id, username = username, email = 'lennon2@thebeatles.com', password = password, first_name = str(test.student_firstname), last_name = test.student_lastname)
            
                send_mail(
                    'CAMELEAN ACADEMY SIS username and pass',
                    "Username: {}\nPassword: {}\nPLEASE CHANGE YOUR USERNAME AND PASSWORD UPON FIRST LOG-IN".format(username, password),
                    None,
                    ['gmgtechdev@gmail.com'],#this is the recipient(change this to email of student later)
                    fail_silently=False,
                )

                return redirect("/RegistrationList")
                False
            else:   
                continue

        ##MAKE A SEPARATE PAGE FOR DISPLAYING USERNAME AND PASS OF EACH USER
    else:
        return render(request,"sis_app/no_access.html")##change this to redirect to loginpage
    # Create your views here.

def updateEnrollmentStatus(request, id):
    test = Student.objects.get(pk = id)
    if test.enrollment_status == "Not Enrolled":
        test.enrollment_status = "Enrolled"
        test.save()
    elif test.enrollment_status == "Enrolled":
        test.enrollment_status = "Not Enrolled"
        test.save()

def paymentForm(request,id=0):
    model = Payment
    form_class = PaymentForm
    if request.method == "GET":
        if id == 0: 
            form = PaymentForm()
        else:
            payment = Payment.objects.get(pk=id)
            form = PaymentForm(instance=payment)
        return render(request,"sis_app/Payment_Form.html",{'form':form})
    else:
        #Values for Varying Student Enrollment Plan
        annual = 37999
        biannual = 38998
        quarterly = 41663

        if id == 0:
            form = PaymentForm(request.POST)
        else:
            payment = Payment.objects.get(pk=id)
            form = PaymentForm(request.POST,instance=payment)
        if form.is_valid():
            form.save()

            s_id = form.cleaned_data['payment_s_account_id']
            payments = Payment.objects.filter(payment_s_account_id = s_id)
            paymentstudentid = Payment.objects.filter(payment_s_account_id = s_id).latest('payment_s_account_id')
            studentID = paymentstudentid.getstudentid()
            studentIDobject = Student.objects.get(pk = studentID)
            test = studentIDobject.student_enrollment_plan
            PaymentOutstandingBalance = Payment.objects.get(outstandingbalance = 0)

            #Update the Initial Outstanding Balance of the student based on the student's enrollment plan
            if test == "Annually":
                Payment.objects.filter(outstandingbalance = 0).update(outstandingbalance = annual)
            elif test == "Bi-Annually":
                Payment.objects.filter(outstandingbalance = 0).update(outstandingbalance = biannual)
            else:
                Payment.objects.filter(outstandingbalance = 0).update(outstandingbalance = quarterly)

            #Get the lowest value for the outstanding balance (The most recently updated outstanding balance based on payments made)
            min = 100000
            for i in payments:
                if i.outstandingbalance < min:
                    min = i.outstandingbalance

            #Subtract payment amount field from the most recent outstanding balance
            if min != 100000:
                test2 = Payment.objects.get(outstandingbalance = min, payment_s_account_id = s_id)
                payment_amount = form.cleaned_data['payment_amount']
                PaymentOutstandingBalance.outstandingbalance = test2.outstandingbalance - payment_amount
                PaymentOutstandingBalance.save()

            updateEnrollmentStatus(request, s_id.id)

        return redirect('/paymentList')

def paymentList(request):

    payments = Payment.objects.all()

    myPFilter = PaymentFilter(request.GET, queryset=payments)
    payments = myPFilter.qs

    print(payments)

    # Payment.objects.filter(getstudentenrollmentstatus="Not Enrolled").update(getstudentenrollmentstatus = "Enrolled")
    

    context = {'paymentList' : payments, 'myPFilter': myPFilter}
    return render(request,"sis_app/paymentList.html", context)

def resetBAEnrollmentStatus(request):
    Student.objects.filter(student_enrollment_plan = "Bi-Annually").update(enrollment_status = "Not Enrolled")
    return redirect('/paymentList')

def resetQEnrollmentStatus(request):
    Student.objects.filter(student_enrollment_plan = "Quarterly").update(enrollment_status = "Not Enrolled")
    return redirect('/paymentList')

def resetALLEnrollmentStatus(request):
    Student.objects.all().update(enrollment_status = "Not Enrolled")
    return redirect('/paymentList')

def EnrollmentStatusAndPaymentPlan(request):
    students = Student.objects.all()

    myFilter2 = EnrollmentStatusAndPaymentPlanFilter(request.GET, queryset=students)
    students = myFilter2.qs

    context = {'studentList' : students, 'myFilter2': myFilter2}
    return render(request,"sis_app/Student_Enrollment.html", context)   

def StudentPaymentView(request):
    user_id = request.user.id
    student = Student.objects.get(pk = user_id)
    paymentstudentid = Payment.objects.filter(payment_s_account_id = user_id).latest('payment_s_account_id')
    student_payments = Payment.objects.filter(payment_s_account_id = user_id)

    context = {"student": student, "payment": paymentstudentid, "payments":student_payments}
    

    return render(request, "sis_app/Student_PaymentView.html", context)

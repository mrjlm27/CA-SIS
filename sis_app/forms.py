from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    student_schoolyear_start:forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
    class Meta:
        model=Student
        fields = ('student_firstname','student_lastname','student_schoolyear_start','student_grade_level', 'enrollment_plan')
        labels = {
            'student_firstname': 'First Name',
            'student_lastname': 'Last Name',
            'student_schoolyear_start':'School Year',
            'student_grade_level':'Grade Level',
            'enrollment_plan': 'Enrollment Plan',
        }

        widgets = {
            'student_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_grade_level': forms.TextInput(attrs={'class': 'form-control'}),
            # 'special_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class LogInForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('username','password')
        labels = {
            'username': 'Username',
            'password': 'Password',
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model=Payment
        fields = ('payment_s_account_id','paymentdate_date','payment_amount')
        labels = {
            'payment_s_account_id': 'Select Student',
            'paymentdate_date': 'Date of Payment',
            'payment_amount': 'Amount of Payment',
        }

        widgets = {
            'paymentdate_date': forms.SelectDateWidget(attrs={'class': 'form-control'}),
            'payment_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
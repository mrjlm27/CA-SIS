from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    student_schoolyear_start:forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
    class Meta:
        model=Student
        fields = ('student_firstname','student_lastname','student_schoolyear_start','student_grade_level')
        labels = {
            'student_firstname': 'First Name',
            'student_lastname': 'Last Name',
            'student_schoolyear_start':'School Year',
            'student_grade_level':'Grade Level',
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
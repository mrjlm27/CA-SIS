from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    student_schoolyear_start:forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
    class Meta:
        model=Student
        fields = ('student_schoolyear_start', 'student_grade_level', 'student_birthday', 
        'student_lastname', 'student_firstname',
        'student_middlename', 'student_nickname',
        'student_address','student_religion', 
        'student_nationality','student_hobbies','student_likes',
        'student_dislikes', 'student_shm','student_allergies',
        'student_sd','student_oconsiderations','student_guardianemail',
        'student_f_firstname','student_f_lastname','student_f_middlename',
        'student_f_telno','student_f_address',
        'student_f_occupation','student_f_employer','student_f_oaddress',
        'student_f_otelno','student_f_natureofbusiness',
        'student_m_firstname','student_m_lastname','student_m_middlename',
        'student_m_telno','student_m_address','student_m_occupation',
        'student_m_occupation','student_m_employer','student_m_oaddress',
        'student_m_otelno','student_m_natureofbusiness',
        'student_sibling_name','student_sibling_gender','student_sibling_age','student_sibling_school',
        'student_medexp','student_rules','student_accuracy',
        'student_signedname','student_signdate', 'student_enrollment_plan'
        )
        labels = {
            'student_firstname': 'First Name',
            'student_lastname': 'Last Name',
            'student_middlename':'Middle Name',
            'student_nickname':'Nickname',
            'student_schoolyear_start':'School Year',
            'student_grade_level':'Grade Level',
            'student_birthday':'Birthday',
            'student_address':'Home Address',
            'student_religion':'Religion',
            'student_nationality':'Nationality',
            'student_hobbies':'Hobbies',
            'student_likes': 'Likes',
            'student_dislikes':'Dislikes',
            'student_shm': 'Special Health Medication',
            'student_allergies':'Allergies',
            'student_sd':'Special Diet',
            'student_oconsiderations':'Anything else that the school should know',
            'student_guardianemail':'''Guardian's Email Address''',
            'student_f_firstname': ''' Father's First Name''',
            'student_f_lastname': '''Father's Last Name''',
            'student_f_middlename':'''Father's Middle Name''',
            'student_f_telno':'''Father's Telephone Number''',
            'student_f_address':'''Father's Home Address''',
            'student_f_occupation':'''Father's Occupation''',
            'student_f_employer':'''Father's Employer''',
            'student_f_oaddress':'''Father's Office Address''',
            'student_f_otelno':'''Father's Office Telephone Number''',
            'student_f_natureofbusiness':'''Father's Nature of Business''',
            'student_m_firstname': ''' Mother's First Name''',
            'student_m_lastname': '''Mother's Last Name''',
            'student_m_middlename':'''Mother's Middle Name''',
            'student_m_telno':'''Mother's Telephone Number''',
            'student_m_address':'''Mother's Home Address''',
            'student_m_occupation':'''Mother's Occupation''',
            'student_m_employer':'''Mother's Employer''',
            'student_m_oaddress':'''Mother's Office Address''',
            'student_m_otelno':'''Mother's Office Telephone Number''',
            'student_m_natureofbusiness':'''Mother's Nature of Business''',
            'student_sibling_name': '''Sibling's Full Name''',
            'student_sibling_gender':'''Sibling's Gender''',
            'student_sibling_age':'''Sibling's Age''',
            'student_sibling_school':'''Sibling's School''',
            'student_medexp':'I hereby authorize Camelean Academy to obtain emergency medical/dental care or emergency evluation for my child at my expense',
            'student_rules':'I hereby been informed of the rules and regulations of Camelean Academy policies as well as it’s primary functions and obligations and I hereby agree to abide by them.The school reserves the right to terminate any enrollee due to bad behavior as well as parents who do not meet school requirements and have unharmonious relationship with school employees',
            'student_accuracy':'I hereby declare that all the information stated above are accurate and complete',
            'student_signedname':'Name',
            'student_signdate':'Date Today',
            'student_enrollment_plan':'Enrollment Plan'
        }

        required = {
            'student_likes': False,
        }

        widgets = {
            'student_schoolyear_start': forms.TextInput(attrs={'class': 'form-control', 'background-color': 'red'}),
            'student_grade_level': forms.Select(attrs={'class': 'form-control'}),
            'student_birthday': forms.DateInput(attrs={'class': 'form-control'}),

            'student_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_lastname': forms.TextInput( attrs={'class': 'form-control'}),

            'student_middlename': forms.TextInput(attrs={'class': 'form-control'}),
            'student_nickname': forms.TextInput( attrs={'class': 'form-control'}),

            'student_address': forms.TextInput(attrs={'class': 'form-control'}),

            'student_religion': forms.TextInput(attrs={'class': 'form-control'}),
            'student_nationality': forms.TextInput( attrs={'class': 'form-control'}),

            'student_hobbies': forms.TextInput(attrs={'class': 'form-control'}),

            'student_likes': forms.TextInput(attrs={'class': 'form-control','required':False}),
            'student_dislikes': forms.TextInput( attrs={'class': 'form-control'}),

            'student_shm': forms.TextInput(attrs={'class': 'form-control'}),
            'student_allergies': forms.TextInput(attrs={'class': 'form-control'}),
            'student_sd': forms.TextInput(attrs={'class': 'form-control'}),
            'student_oconsiderations': forms.TextInput(attrs={'class': 'form-control'}),
            'student_hobbies': forms.TextInput(attrs={'class': 'form-control'}),
            'student_guardianemail': forms.TextInput(attrs={'class': 'form-control'}),

            'student_f_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_f_lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_f_middlename': forms.TextInput(attrs={'class': 'form-control'}),
            'student_f_telno': forms.TextInput(attrs={'class': 'form-control'}),
            'student_f_address': forms.TextInput(attrs={'class': 'form-control'}),
            'student_f_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'student_f_employer': forms.TextInput(attrs={'class': 'form-control'}),
            'student_f_oaddress': forms.TextInput(attrs={'class': 'form-control'}),
            'student_f_otelno': forms.TextInput(attrs={'class': 'form-control'}),
            'student_f_natureofbusiness': forms.TextInput(attrs={'class': 'form-control'}),

            'student_m_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_m_lastname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_m_middlename': forms.TextInput(attrs={'class': 'form-control'}),
            'student_m_telno': forms.TextInput(attrs={'class': 'form-control'}),
            'student_m_address': forms.TextInput(attrs={'class': 'form-control'}),
            'student_m_occupation': forms.TextInput(attrs={'class': 'form-control'}),
            'student_m_employer': forms.TextInput(attrs={'class': 'form-control'}),
            'student_m_oaddress': forms.TextInput(attrs={'class': 'form-control'}),
            'student_m_otelno': forms.TextInput(attrs={'class': 'form-control'}),
            'student_m_natureofbusiness': forms.TextInput(attrs={'class': 'form-control'}),

            'student_sibling_name': forms.TextInput(attrs={'class': 'form-control'}),
            'student_sibling_gender': forms.TextInput(attrs={'class': 'form-control'}),
            'student_sibling_age': forms.TextInput(attrs={'class': 'form-control'}),
            'student_sibling_school': forms.TextInput(attrs={'class': 'form-control'}),

            'student_medexp': forms.CheckboxInput,
            'student_rules': forms.CheckboxInput,
            'student_accuracy': forms.CheckboxInput,

            'student_signedname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_signdate': forms.DateInput(attrs={'class': 'form-control'}),
            'student_enrollment_plan': forms.Select(attrs={'class': 'form-control'}),
            

            # 'student_grade_level': forms.TextInput(attrs={'class': 'form-control'}),
            # 'special_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        def __init__(self,*args,**kwargs):
            super(StudentForm,self).__init__(*args, **kwargs)
            self.fields['student_religion'].required=False
            self.fields['student_middlename'].required=False
            self.fields['student_likes'].required=False
            self.fields['student_shm'].required=False
            self.fields['student_dislikes'].required=False
            self.fields['student_allergies'].required=False
            self.fields['student_sd'].required=False
            self.fields['student_oconsiderations'].required=False
            self.fields['student_f_middlename'].required=False
            self.fields['student_f_otelno'].required=False
            self.fields['student_m_middlename'].required=False
            self.fields['student_m_otelno'].required=False
            self.fields['student_m_otelno'].required=False
            self.fields['student_sibling_name'].required=False
            self.fields['student_sibling_gender'].required=False
            self.fields['student_sibling_age'].required=False
            self.fields['student_sibling_school'].required=False

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
from django import forms
from .models import *

class StudentForm(forms.ModelForm):
    student_schoolyear_start:forms.TypedChoiceField(coerce=int, choices=year_choices, initial=current_year)
    class Meta:
        model=Student
        fields = ('student_firstname','student_lastname','student_middlename',
        'student_nickname','student_schoolyear_start','student_grade_level',
        'student_birthday','student_address','student_religion',
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

        widgets = {
            'student_firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'student_lastname': forms.TextInput(attrs={'class': 'form-control'}),
            # 'student_grade_level': forms.TextInput(attrs={'class': 'form-control'}),
            # 'special_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        def __init__(self,*args,**kwargs):
            super(StudentForm,self).__init__(*args, **kwargs)
            self.fields['student_religion'].required=False
            self.fields['student_middlename'].required=False
            self.fields['student_dislikes'].required=False
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

class GradeReportForm(forms.ModelForm):
    class Meta:
        model=GradeReport
        fields = ('school_year','grading_period','readingreadiness1', 'readingreadiness2', 'readingreadiness3', 'readingreadiness4', 'readingreadiness5', 'readingreadiness6', 'readingreadiness7',
        'readingreadiness8', 'readingreadiness9', 'readingreadiness10', 'readingreadiness11', 'readingreadiness12', 'readingreadiness13',
        'science1','science2','science3' ,'science4','science5','science6', 'language1', 'language2', 'language3', 'language4', 'language5', 'language6',
        'language7', 'language8', 'language9', 'language10', 'math1', 'math2', 'math3', 'math4', 'math5', 'math6', 'math7', 'math8', 'math9', 'math10', 'math11',
        'penmanship1', 'penmanship2', 'penmanship3', 'penmanship4', 'filipino1', 'filipino2', 'filipino3', 'filipino4', 'school_days', 'absences' )
        labels = {
            'school_year':'School Year',
            'grading_period':'Grading Period',
            'readingreadiness1': 'Identifies basic colors and shapes',
            'readingreadiness2': 'Identifies his/her name in a list',
            'readingreadiness3': 'Identifies and names letters of the alphabet',
            'readingreadiness4': 'Identifies and reproduces letter sounds',
            'readingreadiness5': 'Reads with correct pronounciation of sight words',
            'readingreadiness6': 'Reads phrases and sentences using familiar words',
            'readingreadiness7': 'Reads short stories',
            'readingreadiness8': 'Follows one-step direction and instruction',
            'readingreadiness9': 'Relates and remembers details of pictures, events, or stories',
            'readingreadiness10': 'Arranges 2 to 4 pictures of related events in correct sequence',
            'readingreadiness11': 'Completes a logic sequence',
            'readingreadiness12': 'Draws conclusion and predicts outcome',
            'readingreadiness13': 'Grasps the main idea of a picture or of a selection',
            'science1': "Knows how to take care of one's body",
            'science2': "Knows how to take care of one's environment",
            'science3': 'Classifies animals according to their habitat (Land, water, at home, and on leaves)',
            'science4': 'Classifies animals according to their body covering, color, size, number of legs, and movements',
            'science5': 'Classifies objects according to their color, size, shape (solid, liquid, gas) and texture',
            'science6': 'Identifies different weather conditions',
            'language1': 'Has an adequate English speaking vocabulary at his/her level',
            'language2': 'Pronounces CVC words and sight words correctly and clearly',
            'language3': 'Speaks in complete thought patterns',
            'language4': 'Communicates ideas orally',
            'language5': 'Observes correct phrasing and intonation patterns',
            'language6': 'Uses appropriate English expressions and correct grammar in familiar situations',
            'language7': 'Writes CVC words and sight words',
            'language8': 'Converses with ease on particular topics',
            'language9': 'Recites days of the week',
            'language10': 'Recites months of the year in order',
            'math1': 'Knows the concept of sequencing numbers (before, between, after) 0-20, 21-50, 51-100',
            'math2': 'Compares and orders objects according to size, height, length, quantity, etc.',
            'math3': 'Identifies/draws set of familiar objects',
            'math4': 'Identifies/recognizes/writes numeral consisting 0-50 elements/51-100 elements',
            'math5': 'Identifies the ordinal position of objects from first to fifth/sixth to tenth',
            'math6': 'Solves addition wtih 1-digit equations (ex. 9+3 = 12)',
            'math7': 'Solves subtraction with 1-digit equations',
            'math8': 'Solves 2-digit equations',
            'math9': 'Chooses the correct equation (+ or -) for a given situation',
            'math10': 'Writes the correct equation (+ or -) for a given situation',
            'math11': 'Solves simple word problems (+ or -)',
            'penmanship1': 'Follows direciton paths (tracing down broken lines with proper strokes)',
            'penmanship2': "Traces one's name",
            'penmanship3': "Writes one's name",
            'penmanship4': 'Writes words (1st)/ phrases(2nd)/ sentences(3rd) properly',
            'filipino1': 'Pagkilala/Pagsulat ng malaki/maliit na letra ng alpabeto',
            'filipino2': 'Nakakabasa ng salita at maikling kwento',
            'filipino3': 'Pagbuo/Pagsulat ng pantig at salita',
            'filipino4': 'Magkasingkahulugan at Magkasalungat',
            'school_days': 'Number of School Days',
            'absences': 'Number of Absences',
        }

        widgets = {
            'readingreadiness1': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness2': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness3': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness4': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness5': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness6': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness7': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness8': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness9': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness10': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness11': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness12': forms.NumberInput(attrs={'class': 'form-control'}),
            'readingreadiness13': forms.NumberInput(attrs={'class': 'form-control'}),
            'science1': forms.NumberInput(attrs={'class': 'form-control'}),
            'science2': forms.NumberInput(attrs={'class': 'form-control'}),
            'science3': forms.NumberInput(attrs={'class': 'form-control'}),
            'science4': forms.NumberInput(attrs={'class': 'form-control'}),
            'science5': forms.NumberInput(attrs={'class': 'form-control'}),
            'science6': forms.NumberInput(attrs={'class': 'form-control'}),
            'language1': forms.NumberInput(attrs={'class': 'form-control'}),
            'language2': forms.NumberInput(attrs={'class': 'form-control'}),
            'language3': forms.NumberInput(attrs={'class': 'form-control'}),
            'language4': forms.NumberInput(attrs={'class': 'form-control'}),
            'language5': forms.NumberInput(attrs={'class': 'form-control'}),
            'language6': forms.NumberInput(attrs={'class': 'form-control'}),
            'language7': forms.NumberInput(attrs={'class': 'form-control'}),
            'language8': forms.NumberInput(attrs={'class': 'form-control'}),
            'language9': forms.NumberInput(attrs={'class': 'form-control'}),
            'language10': forms.NumberInput(attrs={'class': 'form-control'}),
            'math1': forms.NumberInput(attrs={'class': 'form-control'}),
            'math2': forms.NumberInput(attrs={'class': 'form-control'}),
            'math3': forms.NumberInput(attrs={'class': 'form-control'}),
            'math4': forms.NumberInput(attrs={'class': 'form-control'}),
            'math5': forms.NumberInput(attrs={'class': 'form-control'}),
            'math6': forms.NumberInput(attrs={'class': 'form-control'}),
            'math7': forms.NumberInput(attrs={'class': 'form-control'}),
            'math8': forms.NumberInput(attrs={'class': 'form-control'}),
            'math9': forms.NumberInput(attrs={'class': 'form-control'}),
            'math10': forms.NumberInput(attrs={'class': 'form-control'}),
            'math11': forms.NumberInput(attrs={'class': 'form-control'}),
            'penmanship1': forms.NumberInput(attrs={'class': 'form-control'}),
            'penmanship2': forms.NumberInput(attrs={'class': 'form-control'}),
            'penmanship3': forms.NumberInput(attrs={'class': 'form-control'}),
            'penmanship4': forms.NumberInput(attrs={'class': 'form-control'}),
            'filipino1': forms.NumberInput(attrs={'class': 'form-control'}),
            'filipino2': forms.NumberInput(attrs={'class': 'form-control'}),
            'filipino3': forms.NumberInput(attrs={'class': 'form-control'}),
            'filipino4': forms.NumberInput(attrs={'class': 'form-control'}),
            'school_days': forms.NumberInput(attrs={'class': 'form-control'}),
            'absences': forms.NumberInput(attrs={'class': 'form-control'}),
        }

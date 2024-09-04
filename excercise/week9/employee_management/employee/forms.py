from django import forms
from .models import Position

class EmployeeForm(forms.Form):
    GENDERS = (
        ('-', '------'),
        ("M", "Male"),
        ('F', "Female"),
        ("LGBT", "LGBT")
    )
    first_name = forms.CharField()
    last_name = forms.CharField()
    gender = forms.ChoiceField(choices=GENDERS)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    hire_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    salary = forms.IntegerField(min_value=0)
    position = forms.ModelChoiceField(queryset=Position.objects.all())

    

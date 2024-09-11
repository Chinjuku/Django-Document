from typing import Any
from django import forms
from datetime import date
from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from .models import Employee, Project, Position  # นำเข้า models ที่เกี่ยวข้อง

class EmployeeForm(forms.ModelForm):
    GENDERS = (
        ('-', '------'),
        ("M", "Male"),
        ('F', "Female"),
        ("LGBT", "LGBT")
    )

    gender = forms.ChoiceField(choices=GENDERS)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    hire_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'gender', 'birth_date', 'hire_date', 'salary', 'position']
        

    def clean(self):
        cleaned_data = super().clean()
        hire_date = cleaned_data.get('hire_date')
        if hire_date and hire_date > date.today():
            self.add_error('hire_date', 'Hire date cannot more than today.')
        return cleaned_data

class ProjectForm(ModelForm):

    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    class Meta:
        model = Project
        fields = ["name", "manager", "due_date", "start_date", "description", "staff"]
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        due_date = cleaned_data.get('due_date')
        if start_date and due_date and start_date > due_date:
            self.add_error('start_date', 'Start date cannot be later than the due date.')
        return cleaned_data
    


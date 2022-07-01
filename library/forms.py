from dataclasses import field
from django.forms import ModelForm,widgets
from .models import Book,Student
from django.contrib.auth.models import User
from . import models
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

class BookForm(ModelForm):
    class Meta:
        model  = Book
        fields=['name','isbn','author','category','status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.NumberInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'statu': forms.CheckboxInput(attrs={'class': 'form-control'}),

        }

       # widgets={
       #     'status':forms.CheckboxSelectMultiple(), 
       # }

       # def __init__(self, *args,  **kwargs):
        #    super(BookForm, self).__init__(*args,  **kwargs)

        #    for name , field in self.fields.items():
        #        field.widget.attrs.update({'class':'wrapper'})

          #  self.fields['name'].widget.attrs.update({'class':'input'})
    
    

class StudentUserForm(ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),

        }


class StudentExtraForm(ModelForm):
    class Meta:
        model= Student
        fields=['department','semester','roll_no','image','gender','contact','email','address','status']
        widgets = {
            'department': forms.TextInput(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'roll_no': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'contact': forms.NumberInput(attrs={'class': 'form-control'}),

        }


class IssuedBookForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    isbn2=forms.ModelChoiceField(queryset=models.Book.objects.all(),empty_label="Name and isbn", to_field_name="isbn",label='Name and Isbn')
    semester2=forms.ModelChoiceField(queryset=models.Student.objects.all(),empty_label="Name and semester",to_field_name='semester',label='Name and semester')
    

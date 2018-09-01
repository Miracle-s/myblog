from django.db import models
from django import forms
from django.contrib.auth.models import User
from .models import UserInfo, Code
from django.forms import widgets

class LoginForm(forms.Form):
    username = forms.CharField(widget=widgets.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=widgets.PasswordInput(attrs={'class':"form-control",})) 
    password2 = forms.CharField(widget=widgets.PasswordInput(attrs={'class':"form-control",}))
    username = forms.CharField(widget=widgets.TextInput(attrs={'class':'form-control',}))
    code = forms.CharField(widget=widgets.TextInput(attrs={'class':"form-control",}))
    email = forms.CharField(widget=widgets.EmailInput(attrs={'class':'form-control',}))
    class Meta:
        model = User
        fields = ("username","email","is_active")

    def clean_email(self):
        cd = self.cleaned_data
        email = cd['email']
        user = User.objects.filter(email=email).first()
        if user:
            raise forms.ValidationError('邮箱已被注册！')
        return cd['email']

    def clean_code(self):
        cd = self.cleaned_data
        codes = Code.objects.all()
        for code in codes:
            if cd['code'] == code.code and not code.is_used:
                return cd['code']
        raise forms.ValidationError('code error')
        
    def clean_password2(self):
        cd = self.cleaned_data
        if len(cd['password']) <= 7:
            raise forms.ValidationError('password to short, 8')

        if cd['password'] != cd['password2']:
            raise forms.ValidationError("passowrds do not match")
        return cd['password2']
    


class UserInfoForm(forms.ModelForm):
    phone = forms.CharField(widget=widgets.TextInput(attrs={"class":"form-control"}),required=False)
    school = forms.CharField(widget=widgets.TextInput(attrs={"class":"form-control"}),required=False)
    company= forms.CharField(widget=widgets.TextInput(attrs={"class":"form-control"}),required=False)
    profession= forms.CharField(widget=widgets.TextInput(attrs={"class":"form-control"}),required=False) 
    address = forms.CharField(widget=widgets.TextInput(attrs={"class":"form-control"}),required=False)
    aboutme = forms.CharField(widget=widgets.Textarea(attrs={"class":"form-control",'rows':4}),required=False)    
 
    class Meta:
        model = UserInfo
        fields = ("phone",'school','company','profession','aboutme','photo')

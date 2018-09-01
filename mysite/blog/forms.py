from django.db import models
from django import forms
from django.contrib.auth.models import User
from .models import ArticleColumn, Article

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title","bref","body")

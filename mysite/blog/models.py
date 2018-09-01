from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse

# Create your models here.

class Category(models.Model):
    category = models.CharField(max_length=20)
    c_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.category

class ArticleColumn(models.Model):
    #user = models.ForeignKey(User, related_name="article_column")
    user = models.ManyToManyField(User, related_name="article_column")
    column = models.CharField(max_length=20)
    category = models.ForeignKey(Category, related_name="article_column")
    c_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.column


class Article(models.Model):
    author = models.ForeignKey(User, related_name="article")
    column = models.ForeignKey(ArticleColumn, related_name="article")
    title = models.CharField(max_length=200)
    bref = models.CharField(max_length=200)
    body = models.TextField()
    c_date = models.DateTimeField(default=timezone.now())
    u_date = models.DateTimeField(auto_now=True)
    num_read = models.IntegerField(default=1)
    num_good = models.IntegerField(default=1)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("blog:article_detail", args=[self.id,])


class Comment(models.Model):
    author = models.ForeignKey(User,related_name="comment")
    title = models.CharField(max_length=200)
    body = models.TextField()
    c_date = models.DateTimeField(default=timezone.now())
    parent = models.ForeignKey('self',related_name="children",default=None,blank=True,null=True)
    
    def __str__(self):
        return self.title
    

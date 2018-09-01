from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Code(models.Model):
    code = models.CharField(max_length=20,)
    is_used = models.BooleanField(default=False)
    c_date = models.DateField(auto_now_add=True)


class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    school = models.CharField(max_length=20, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    profession = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    aboutme = models.TextField(blank=True, null=True)
    photo = models.ImageField(blank=True, null=True)

    def __str__(self):
        return 'user:{}'.format(self.user.username)


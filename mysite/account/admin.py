from django.contrib import admin
from .models import Code, UserInfo
# Register your models here.

class CodeAdmin(admin.ModelAdmin):
    list_display = ('code','is_used','c_date')

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('user','phone','school','company','profession')


admin.site.register(Code, CodeAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
    

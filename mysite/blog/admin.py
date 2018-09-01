from django.contrib import admin
from .models import Category,ArticleColumn, Article

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category','c_date')

class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ('column','category' ,'c_date')
    ordering = ['category','column','c_date']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','column','author','c_date')
    list_filter = ('title','author')
    list_fields = ('title','body')
    ordering = ['title','author']

admin.site.register(Category,CategoryAdmin)
admin.site.register(ArticleColumn, ArticleColumnAdmin)
admin.site.register(Article, ArticleAdmin)

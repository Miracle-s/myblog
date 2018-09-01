from django.views.generic import View
from .models import Article,Category,ArticleColumn
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .forms import ArticlePostForm
from django.views.decorators.csrf import csrf_exempt
import time
search = None

def get_most_like(num):
    return Article.objects.all().order_by('-num_read')[:num]

def get_most_new(num):
    return Article.objects.all().order_by('-c_date')[:num]

def get_pre_nex(article):
    articles = article.column.article.all().order_by('id')
    cur = 0
    for art in articles:
        if article.id == art.id:
            break
        cur +=1
    if cur != 0:
        pre = articles[cur-1].id
    else:
        pre = None
    if len(articles) == cur+1:
        nex = None
    else:
        nex = articles[cur+1].id
    return (pre,nex)
        

def pageFunc(request,articles):
    #3条数据为一页，多余0条则新开一页
    paginator = Paginator(articles,3,0)
    page = request.GET.get('page')
    if page: 
        return paginator.page(page)
    else:
        return paginator.page(1)

def columnF(request,column_id):
    num =5
    most_like_arts = get_most_like(5)
    most_new_arts = get_most_new(5)
    if not column_id:
        info_category = '该模块还没有文章，请联系管理员！！'
        return render(request, 'home.html',{'info_category':info_category,'most_like_arts':most_like_arts,'most_new_arts':most_new_arts})
    column = ArticleColumn.objects.filter(id=column_id).first()
    if not column:
        info_category = '抱歉请输入正确的网址！！！'
        return render(request, 'home.html',{'info_category':info_category,'most_like_arts':most_like_arts,'most_new_arts':most_new_arts})
    else:
        columns = column.category.article_column.all()
        articles = column.article.all()
        if not articles:
            info_column = '该栏目还没有文章，请联系管理员！！'
            return render(request, 'home.html',{'info_column':info_column,'most_like_arts':most_like_arts,'most_new_arts':most_new_arts,'columns':columns,'column':column})
        else:
            cus_list = articles = pageFunc(request,articles)
            return render(request, 'home.html',{'columns':columns,'column':column,'articles':articles,'cus_list':cus_list,'most_like_arts':most_like_arts,'most_new_arts':most_new_arts})


def search(request):
    cus_list  = articles =None
    info_category = None
    column =None
    columns = ArticleColumn.objects.all()
    if request.GET.get('page'):
        global search
    else:
        search =  request.GET.get('search')
    if not search:
        info_category = "请输入关键字"
        columns = None
    else:
        articles = Article.objects.filter(title__icontains=search)
        if not articles:
            info_category = "抱歉，没有搜索到'{}'相关的内容".format(search)
            columns = None
        else:
            column = articles.first().column
            cus_list = articles = pageFunc(request,articles)
    most_like_arts = get_most_like(5)
    most_new_arts = get_most_new(5)
    return render(request, 'home.html', {'search':search,'column':column,'columns':columns,'info_category':info_category, 'cus_list':cus_list,"articles":articles,'most_like_arts':most_like_arts,'most_new_arts':most_new_arts})


def category(request, category_id):
    category = Category.objects.filter(id=category_id).first()
    column = category.article_column.all()
    if column:
        return columnF(request,column[0].id)
    else:
        return columnF(request,0)
    


def home(request):
    return render(request, 'home.html')

class ArticleDetail(View):
    def get(self, request, article_id):
        article = Article.objects.filter(id=article_id).first()
        num =5
        if article :
            article.num_read +=1
            article.save()
            art_pre, art_next = get_pre_nex(article)
            userInfo = article.author.userinfo
        else:
            article = "文章不存在"
            art_pre = art_next = None
            userInfo = None
        most_like_arts = get_most_like(num)
        most_new_arts = get_most_like(num)
        return render(request, 'blog/article_detail.html', {'userInfo':userInfo,"article":article,'most_like_arts':most_like_arts,'most_new_arts':most_new_arts,'art_pre':art_pre,'art_next':art_next})


@login_required(login_url='/account/login')
@csrf_exempt
def article_post(request,*args):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        article_id = request.POST.get('article_id')
        if article_post_form.is_valid() and article_id == '-1':
            cd = article_post_form.cleaned_data
            try:
                new_article = article_post_form.save(commit=False)
                new_article.author = request.user
                column = ArticleColumn.objects.get(id=request.POST['column_id'])
                if column in request.user.article_column.all():
                    #直接创建
                    new_article.column = column
                else:
                    #将user添加到column中
                    column.user.add(request.user)
                    column.save()
                new_article.column = column
                new_article.save()
                return HttpResponse('1')
            except Exception as e:
                print(e)
                return HttpResponse('2')
        elif article_post_form.is_valid():
            try:
                article = Article.objects.filter(id=article_id).first()
                article.title = request.POST.get('title')
                article.body = request.POST.get('body')
                article.bref = request.POST.get('bref')
                article.column = ArticleColumn.objects.filter(id=request.POST.get('column_id')[0]).first()
                article.save()
                return HttpResponse(1)
            except Exception as res:
                print(res)
                return HttpResponse('2')
        else:
            return HttpResponse('3')
    else:
        article_post_form = ArticlePostForm()
        article_columns = ArticleColumn.objects.all()
        article_id = -1
        return render(request,"blog/article_post.html", {"article_post_form":article_post_form,"article_columns":article_columns,'article_id':article_id})
        

@login_required(login_url="account/login")
def article_edit(request, article_id):
    article = Article.objects.filter(id=article_id).first()
    if article:
        if request.user == article.author:
            article_post_form = ArticlePostForm(data={"title":article.title,"bref":article.bref,"column":article.column,"body":article.body})
            article_columns = ArticleColumn.objects.all()
            return render(request, "blog/article_post.html", {"article_post_form":article_post_form, "article_columns":article_columns,"article_id":article_id})
        else:
            return HttpResponse("非文章作者，不能修改文章！！")
    else:
        return HttpResponse("没有对应的文章，请重试！！")

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Article, Account
import re


# Create your views here.
def index(request):
    '''The main page'''
    template = loader.get_template('blog/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


# /article
def articles(request):
    '''The article exhibition page'''

    template = loader.get_template('blog/article.html')
    # a = Article.objects.all()
    # context = {'articles': a}
    username = request.session.get('user')
    if username:
        context = {'user': username}
    else:
        context = {'user': "LOGIN"}
    return HttpResponse(template.render(context, request))


# /developing
def developing(request):
    '''The notification for unfinished pages'''
    template = loader.get_template('blog/developing.html')
    context = {}
    return HttpResponse(template.render(context, request))


# /message
def message(request):
    '''The notification for unfinished pages'''
    template = loader.get_template('blog/message.html')
    username = request.session.get('user')
    if username:
        context = {'user': username}
    else:
        context = {'user': "LOGIN"}
    return HttpResponse(template.render(context, request))


# /article_read
def article_read(request, article_id):
    template = loader.get_template('blog/article_read.html')
    a = Article.objects.get(id=article_id)
    context = {'article': a}
    return HttpResponse(template.render(context, request))


# /login
def login(request):
    template = loader.get_template('blog/login.html')
    # a = Article.objects.get(id=article_id)
    # context = {'article': a}
    context = {}
    return HttpResponse(template.render(context, request))


# /login
def logout(request):
    del request.session['user']
    return redirect('/article')


# /sign_up
def sign_up(request):
    template = loader.get_template('blog/sign_up.html')
    # a = Article.objects.get(id=article_id)
    # context = {'article': a}
    context = {}
    return HttpResponse(template.render(context, request))


def login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    a = Account.objects.filter(username=username)
    if a and a[0].password == password:
        # return 1 when success
        request.session['user'] = username
        request.session.set_expiry(3600*24*2)
        return JsonResponse({'res': 1})
    else:
        # return 0 when there is an error

        return JsonResponse({'res': 0})


def sign_up_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_check = request.POST.get('password_check')
    ret_username = re.match(r'^[a-zA-Z0-9_]{4,20}$', username)
    ret_password = re.match(r'^[^ ]{4,20}$', password)
    if ret_username:
        if username != 'rhine':
            if password == password_check:
                if ret_password:
                    a = Account()
                    a.username = username
                    a.password = password
                    a.save()
                    request.session['user'] = username
                    # 1: ok
                    return JsonResponse({'res': 1})
                else:
                    # 2: invalid character
                    return JsonResponse({'res': 2})
            else:
                # 3: passwords don't match
                return JsonResponse({'res': 3})
        else:
            # 4: username is taken
            return JsonResponse({'res': 4})
    else:
        # 5: username is invalid
        return JsonResponse({'res': 5})



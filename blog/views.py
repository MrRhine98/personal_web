from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from .models import Article, Account
import re
import markdown


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


# /read
def read(request):
    template = loader.get_template('blog/read.html')
    a = '''[TOC]
# git note
## Basics
### 添加文件
```python
git add file.py
git rm file.py
git commit -m 'version_desc'
```

### 查看版本
```python
git log --graph
# 显示时间线
git log --pretty=oneline
# 单行显示
git reflog
# 操作记录
```

### 回退版本
```python
git reset --hard HEAD^
git reset --hard HEAD~1
git reset --hard 8b4h3k12ki239khbe
# 版本号
```
`HEAD`指向当前版本  
`HEAD^`指向前一个版本，等价于`HEAD~1`
多个版本回退使用`HEAD~num`或`HEAD^^^`

### 状态查询
```python
git status
```

### 撤销修改
```python
git checkout -- code.txt
```
撤销工作区未添加到暂存区的修改
```python
git reset HEAD code.txt
```
撤销暂存区中的修改，工作区的修改仍然存在

### 对比文件
```python
git diff HEAD -- code.txt
```
对比当前工作区和最近版本中的code.txt文件的区别
```python
git diff HEAD HEAD^ code.txt
```
对比当前版本和上一版本中的code.txt文件的区别

## Branch
### 创建以及查看分支
```python
git checkout -b branch_name
# 创建一个名为branch_name的分支，并切换到该分支
git checkout branch_name
# 切换到branch_name的分支
git branch
# 查看当前存在的分支
```

### 合并以及删除分支
```python
git merge branch_name
# 快速合并（fast forward）branch_name分支
git merge --no-ff -m 'no fast forward' branch_name
# 禁用快速合并
git branch -d branch_name
# 删除branch_name分支
```

### 工作现场保存
```python
git stash
# 保存当前工作环境
git stash list
# 查看已保存的工作环境
git stash pop
# 加载工作环境
```

## Github
### 添加ssh账户
家目录下编辑.gitconfig文件，添加邮箱和用户名
```python
[user]
	name = MrRhine98
	email = rick9809@gmail.com
```
生成ssh密钥，储存于home目录下.shh文件夹下.
`id_rsa`为公钥，`id_rsa.pub`为公钥
```python
ssh-keygen -t rsa -C "rick9809@gmail.com"
```

### 克隆项目
```python
git clone ssh路径
```

### 推送
推送分支到服务器
```python
git push origin branch_name
```

### 跟踪远程分支
```python
git branch --set-upstream-to=origin/branch_name branch_name
```
远程提交
```python
git push
```

### 从远程分支拉取代码
```python
git pull origin branch_name
```
将远程拉取下来并合并到本地分支

### 将本地代码提交为新代码库
```python
git remote add origin 'ssh address'
```
删除origin终端
```python
git remote rm origin
```
'''
    content = markdown.markdown(a, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    context = {'article': content}
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


# /save_article
def save_article(request):
    title = request.POST.get('title')
    content = request.POST.get('editorContent')
    a = Article()
    a.atitle = title
    a.acontent = content
    a.save()
    return redirect('/')

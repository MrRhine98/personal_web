from django.urls import path
from blog import views

app_name = 'blog'
urlpatterns = [
    path('login', views.login, name='login'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('article', views.articles, name='article'),
    path('article/<int:article_id>', views.article_read, name='article_read'),
    path('', views.index, name='index'),
    path('developing', views.developing, name='developing'),
    path('message', views.message, name='message'),
    path('login_check', views.login_check, name='login_check'),
    path('sign_up_check', views.sign_up_check, name='sign_up_check'),
    path('logout', views.logout, name='logout'),

]
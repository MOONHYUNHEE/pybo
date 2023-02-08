'''
파일명: urls.py
설명: common의 urls (로그인/ 로그아웃 구현)
생성일 : 2023-02-06
생성자: judge
since 2023.01.09 Copyright (c) by KandJang All right reserved.
'''
from django.urls import path
from django.contrib.auth import views as auth_views
from .import views

app_name = 'common'
urlpatterns = [
    # django.contrib.auth앱의 LoginView 클래스를 활용
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    # logout: LogoutView
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # signup: 회원가입
    path('signup/', views.signup, name='signup')

]


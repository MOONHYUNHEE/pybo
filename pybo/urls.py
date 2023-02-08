'''
파일명: urls.py
설명: pybo 모든 URL과 view함수의 매핑 담당
생성일 : 2023-01-25
생성자: judge
since 2023.01.09 Copyright (c) by KandJang All right reserved.
'''


from django.urls import path
from . import views  # 현재 디렉토리에 views 모듈을 갖다 놓음

app_name = 'pybo'

urlpatterns = [

    path('', views.index, name='index'),  # views index로 매핑
    # 질문 detail
    path('<int:question_id>/', views.detail, name='detail'),
    # 질문 만들기
    path('question/create/', views.question_create, name='question_create'),
    # 질문수정
    path('question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    # 질문삭제
    path('question/delete/<int:question_id>/', views.question_delete, name='question_delete'),

    #answer
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),


    #template menu
    path('boot/menu/', views.boot_menu, name='boot_menu'),
    #bootstrap template
    path('boot/list/', views.boot_list, name='boot_list'),
    path('boot/reg/', views.boot_reg, name='boot_reg'),
    #Crawling
    path('crawling/cgv/', views.crawling_cgv, name='crawling_cgv'),



]
'''
파일명 : urls.py
설 명 :  board url
생성일 : 2023-02-14
생성자 : user
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''
from django.contrib import admin
from django.urls import path,include
from board.views import base_views,board_views

app_name = 'board'

urlpatterns = [
    #base_view
    path('',base_views.index,name='index'), #view index로 메핑
    path('<int:board_id>/', base_views.detail, name='detail'), #board상세

    #board
    path('create/',board_views.create, name='create'),
    path('modify/',board_views.modify, name='modify'),
    path('delete/',board_views.delete, name='delete'),

]
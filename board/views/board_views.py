'''
파일명 : board_views.py
설 명 :
생성일 : 2023-02-15
생성자 : user
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''


import logging


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from board.models import Board
from ..forms import BoardForm
from django.contrib import messages

@login_required(login_url='common:login') #로그인이 되어있지 않으면 login페이지로 이동
def delete(request):
    '''  수정 : login 필수'''
    logging.info('1. modify')
    board_id = request.POST.get('id')  # 페이지
    logging.info('2. board_id:{}'.format(board_id))

    board = get_object_or_404(Board, pk=board_id)  # question id로 Question조회

    # 권한 check
    if request.user != board.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('board:detail', board_id=board.id)

    logging.info('3.delete post')

    board.delete() #삭제
    return redirect('board:index')


@login_required(login_url='common:login') #로그인이 되어있지 않으면 login페이지로 이동
def modify(request):
    '''  수정 : login 필수'''
    logging.info('1. modify')

    board_id = request.POST.get('id')  # 페이지
    subject = request.POST.get('subject')  # 페이지
    content = request.POST.get('content')  # 페이지

    logging.info('2. board_id:{}'.format(board_id))
    logging.info('2. subject:{}'.format(subject))
    logging.info('2. content:{}'.format(content))

    board = get_object_or_404(Board, pk=board_id)  # question id로 Question조회

    # 권한 check
    if request.user != board.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('board:detail', board_id=board.id)

    logging.info('3.modify post')

    board.subject = subject
    board.content = content
    board.modify_date = timezone.now()  # 수정일시 저장
    board.save()  # 수정일시 까지 생성해서 저장(Commit)
    return redirect('board:index')

@login_required(login_url='common:login') #로그인이 되어있지 않으면 login페이지로 이동
def create(request):
    logging.info('1. board_create')
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board=form.save(commit=False)
            board.create_date = timezone.now()
            board.author = request.user  # author 속성에 로그인 계정 저장
            board.save()
            return redirect('board:index')
    else:
        form = BoardForm()

    context = {'form':form}
    logging.info('2. form')
    return render(request,'board/board_form.html',context)

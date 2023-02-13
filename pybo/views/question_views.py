'''
파일명: question_views.py
설명: 질문관리
생성일 : 2023-02-08
생성자: judge
since 2023.01.09 Copyright (c) by KandJang All right reserved.
'''
import logging

# 메시지를 담을 수 있는 객체를 만들기 위해 import
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# ctrl+alt+o : import 정리
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from ..forms import QuestionForm
from ..models import Question

@login_required(login_url='common:login')
def question_vote(request,question_id):
    logging.info('1. question_id:{}'.format(question_id))
    question = get_object_or_404(Question, pk=question_id)

    if request.user == question.author:
        logging.info('2. question.author:{}'.format(question.author))
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    else:
        logging.info('2. else request.user:{}'.format(request.user))
        question.voter.add(request.user)
    return redirect('pybo:detail', question_id=question.id)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def question_modify(request, question_id):
    logging.info('1. question_id:{}'.format(question_id))
    question = get_object_or_404(Question, pk=question_id)

    logging.info('2. question.id:{}'.format(question.id))

    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_create(request):
    '''질문등록  위는 POST 방식  아래는 Get 방식 '''
    logging.info('1.requestion.method:{}'.format(request.method))
    if request.method == 'POST':
        logging.info('2.question_create post')
        # 저장
        form = QuestionForm(request.POST)  #request.POST 데이터 (subject, content 자동 생성)
        logging.info('3.question_create post')

        if form.is_valid(): # 폼(질문등록)이 유효하면 저장해라
            logging.info('4.form.is_valid:{}'.format(form.is_valid()))
            question = form.save(commit=False)  # subject, content만 저장(확정commit은 하지 않음)
            question.author = request.user  # author 속성에 로그인 계정 저장
            question.create_date = timezone.now()
            question.author=request.user
            question.save() # 날짜까지 생성해서 저장(commit)
            return redirect("pybo:index")
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'pybo/question_form.html',context)
# context = {'question': question}  == {'form':form}



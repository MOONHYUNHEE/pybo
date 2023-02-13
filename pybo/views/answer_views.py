'''
파일명: answer_views.py
설명: 답변관리
생성일 : 2023-02-08
생성자: judge
since 2023.01.09 Copyright (c) by KandJang All right reserved.
'''
import logging

# 메시지를 담을 수 있는 객체를 만들기 위해 import
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
# ctrl+alt+o : import 정리
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone
from ..forms import AnswerForm
from ..models import Question, Answer

@login_required(login_url='common_login')
def answer_vote(request, answer_id):
    answer=get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '본인 작성한 글은 추천할 수 없습니다.')
    else:
        answer.voter()
    return redirect('{}#answer_{}'.format(
        resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        answer.delete()
    return redirect('pybo:detail', question_id=answer.question.id)

@login_required(login_url='common:login')
def answer_modify(request,answer_id):
    logging.info('1.answer_modify:{}'.format(answer_id))
    #1. answer id에 해당되는 데이터 조회
    #2. 수정 권한 체크: 권한이 없는 경우 메시지 전달
    #3-1. POST : 수정
    #3-2. GET: 수정 Form 만들어서 전달

    #1.
    answer=get_object_or_404(Answer, pk=answer_id)
    #2.
    if request.user != answer.author:
        messages.error(request,'수정권한이 없습니다.')
        #수정 화면
        return redirect('pybo:detail',question_id=answer.question.id)
    #3.
    if request.method == "POST":        # 수정
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer=form.save(commit=False)
            answer.modify_date=timezone.now()
            logging.info('3.answer_modify')
            answer.save()
            # 수정 화면
            return redirect('pybo:detail', question_id=answer.question.id)
    else:                               #수정 form의 template
        form = AnswerForm(instance=answer)
    context={'answer':answer, 'form':form}
    return redirect('{}#answer_{}'.format(
        resolve_url('pybo:detail', question_id=answer.question.id), answer.id))

@login_required(login_url='common:login')
def answer_create(request, question_id):
    '''답변 등록'''
    logging.info('answer_create question_id:{}'.format(question_id))
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)  #content만 저장 (commit은 하지 않음)
            answer.author = request.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()  # 날짜까지 생성해서 저장
            return redirect('{}#answer_{}'.format(
                resolve_url('pybo:detail', question_id=question.id), answer.id))
    else:
        return HttpResponseNotAllowed('Post만 가능합니다.')
    context = {'question': question, 'form':form }
    return render(request,'pybo/question_detail.html',context)


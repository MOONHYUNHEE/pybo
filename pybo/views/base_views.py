'''
파일명: base_views.py
설명: 기본관리
생성일 : 2023-02-08
생성자: judge
since 2023.01.09 Copyright (c) by KandJang All right reserved.
'''
import logging

# ctrl+alt+o : import 정리
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from ..models import Question


# 메시지를 담을 수 있는 객체를 만들기 위해 import

def detail(request, question_id):
    '''Question 상세'''
    logging.info('1. question_id:{}'.format(question_id))
    # question=Question.objects.get(id=question_id)
    question = get_object_or_404(Question, pk=question_id)

    logging.info('2. question:{}'.format(question))
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)


# logger = logging.getLogger('pybo')
# Create your views here.
#index함수 만들기
def index(request):
    '''Question 목록'''
    #list order create_date desc
    # logging.info('index 레벨로 출력')
    # print('index 레벨로 출력')

    # 입력인자
    page=request.GET.get('page', '1') # 페이지
    logging.info('page:{}'.format(page))

    question_list = Question.objects.order_by('-create_date') #DSC / 마이너스 빼면 ASC
    # question_list = Question.objects.filter(id=99)
    #paging
    paginator=Paginator(question_list,10)
    page_obj=paginator.get_page(page)
    #속성 - paginator.count : 전제 게시물 개수
    #속성 - paginator.per_page : 페이지당 보여줄 게시물 개수
    #속성 - paginator.page_range : 페이지 범위
    #속성 - paginator.number : 현재 페이지 번호
    #속성 - paginator.previous_page_number : 이전 페이지 번호
    #속성 - next_previous : 다음 페이지 번호
    #속성 - has_previous : 이전 페이지 유무
    #속성 - has_next : 다음 페이지 유무
    #속성 - start_index : 현재 페이지 시작 인덱스(1부터 시작)
    #속성 - end_index : 현재 페이지 끝 인덱스


    context = {'question_list': page_obj}
    logging.info('question_list:{}'.format(page_obj))


    # context = {'question_list': question_list}
    # print('question_liste:{}')
    return render(request,'pybo/question_list.html',context)



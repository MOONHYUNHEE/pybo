#ctrl+alt+o : import 정리
import logging
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse,HttpResponseNotAllowed
from django.utils import timezone
from .models import Question,Answer
from .forms import QuestionForm, AnswerForm
import logging
from bs4 import BeautifulSoup
import requests
from django.contrib.auth.decorators import login_required

# 메시지를 담을 수 있는 객체를 만들기 위해 import
from django.contrib import messages

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
    return render(request, 'pybo/answer_form.html',context)
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


def crawling_cgv(request):
    '''cgv 무비차트'''
    url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
    response = requests.get(url)
    context = {}

    if 200 == response.status_code:
        html=response.text
        # print('html:{}'.format(html))
        # box-contents
        soup=BeautifulSoup(html,'html.parser')
        # 영화명
        title = soup.select('div.box-contents strong.title')
        # 예매율
        reserve = soup.select('div.score strong.percent span')
        # 포스터]
        poster = soup.select('span.thumb-image img')

        title_list =[] # 제목
        reserve_list = [] # 예매율
        poster_list = [] # 포스터
        for page in range(0,7,1):
            posterImg = poster[page]
            imgUrlPath=posterImg.get('src') # get으로 attribute(속성) 접근 가능  ex) <img src=''> 에 접근
            # print('imgUrlPath:{}'.format(imgUrlPath))
            title_list.append(title[page].getText())
            reserve_list.append(reserve[page].getText())
            poster_list.append(imgUrlPath)
            print('title[page]:{},{},{}'.format(title[page].getText()
                                                    ,reserve[page].getText()
                                                    ,imgUrlPath
                                                    ))

            pass
        #화면에 title을 []전달
            # context = {'title': title_list, 'reserve':reserve_list,'post_list':poster_list}
            context={'context':zip(title_list, reserve_list, poster_list)}
    else:
        print('response.status_code:{}'.format(response.status_code))
    pass
    return  render(request, 'pybo/crawling_cgv.html', context)

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

def boot_reg(request):
    '''bootstrap reg'''
    return render(request, 'pybo/reg.html')
# bootstrap list
def boot_menu(request):
    '''개발에 사용되는 임시 메뉴'''
    return render(request, 'pybo/menu.html')

def boot_list(request):
    '''bootstrap template'''
    return render(request, 'pybo/list.html')

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
            return redirect('pybo:detail', question_id=question_id)
    else:
        return HttpResponseNotAllowed('Post만 가능합니다.')
    context = {'question': question, 'form':form }
    return render(request, 'pybo/question_detail.html', context)

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



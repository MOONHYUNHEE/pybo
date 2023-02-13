'''
파일명: pybo_filter.py
설명: 빼기 필터
생성일 : 2023-02-03
생성자: judge
since 2023.01.09 Copyright (c) by KandJang All right reserved.
'''

from django import template
import markdown
from django.utils.safestring import mark_safe
register = template.Library()
@register.filter
def sub(value, arg):
    ''' @register.filter:템플릿에서 필터로 사용할수 있게 된다.
        빼기 필터
    '''
    return value - arg
@register.filter
def mark(value):
    extensions = ["nl2br","fenced_code"]
    return mark_safe(markdown.markdown(value,extensions=extensions))

def index(request):
    '''question 목록'''
    # list order create_date desc
    # logging.info('index 레벨로 출력')
    # 입력인자: http://127.0.0.1:8000/pybo/2
    #view-source:http://127.0.0.1:8000/?kw=%EA%B8%88%EC%9A%94%EC%9D%BC&page=1
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 페이지
    logging.info('page:{}'.format(page))
    logging.info('kw:{}'.format(kw))
    question_list = Question.objects.order_by('-create_date')  # order_by('-필드') desc, asc order_by('필드')
    #subject__contains : 사용 __contains또는 __icontains(대소 문자 구분) :
    question_list = question_list.filter(subject__contains=kw)
    # paging
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    # question_list = Question.objects.filter(id=99)  # order_by('-필드') desc, asc order_by('필드')
    context = {'question_list': page_obj,'kw':kw, 'page':page}
    logging.info('question_list:{}'.format(page_obj))
    return render(request, 'pybo/question_list.html', context)
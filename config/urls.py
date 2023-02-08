"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from pybo.models import Question, Answer
from django.utils import timezone


# #데이터 생성 및 저장
# q=Question(subject='파이썬 게시판은 무엇인가요?', content='알고 싶어요!', create_date=timezone.now())
# q=Question(subject='장고 모델은 무엇인가요?', content='id는 자동으로 생성되나요', create_date=timezone.now())
# q.save()

# 데이터 모두 추출
# Question.objects.all()

# 데이터 수정 : 조회 -> 출력 > 수정 > 저장 > 출력
# q = Question.objects.get(id=2) # 조회
# q # 출력
# q.subject = 'Django Model Question' # 수정
#q.save() 저장 -> q (출력)

# 데이터 삭제 : 데이터 조회 > 삭제 (삭제 시 삭제한 데이터 리던해줌)
# q = Question.objects.get(id=1)  # 조회
# q.delete() # 삭제

#Answer 연결된 데이터 관리 : Question에 데이터 조회 > answer 생성 및 저장 > answer 조회
# q = Question.objects.get(id=2)
# a=Answer(question=q, content='id는 자동생성됩니다.', create_date=timezone.now())
# a.save()

# 데이터 조회
# a = Answer.objects.get(id=1)
# a

#question 데이터조회(연결된 데이터 조회)
# a.question  # 출력 결과 : <Question: Django Model Question>
# #Question에서 Answer 답변 조회
# q.answer_set.all() # 출력 결과 : <QuerySet [<Answer: Answer object (1)>]>

from django.contrib import admin
from django.urls import path,include
from pybo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('pybo/', views.index),
    path('pybo/', include('pybo.urls')),  #pybo로 요청 들어오면 urls가 처리한다.
    path('common', include('common.urls')),
    # common로 요청 들어오면 urls가 처리한다.
    path('',views.index, name='index')
]

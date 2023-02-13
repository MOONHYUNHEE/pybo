from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# 질문 클래스(테이블)  생성 : subject, content, create_date (장고 - 키 값 넣지 않고 생성 시 자동으로 키 값 생성됨)
class Question(models.Model):
    subject = models.CharField(max_length=200) # max_length = 글자수 제한
    content = models.TextField() # 글자수 제한 없는 컬럼
    create_date = models.DateTimeField() # 날짜 + 시간

    # author필드 추가: 글쓴이
    author=models.ForeignKey(User,on_delete=models.CASCADE, related_name='author_question')  #회원테이블에 사용자 정보가 삭제되면  Question 테이블의 질문정보도 같이 삭제

    #수정일시 추가
    modify_date = models.DateTimeField(null=True, blank=True)
    # 데이터 베이스에서 null 허용,form

    #추천 (다대다 관계 표시 필드 추가 )
    voter = models.ManyToManyField(User, related_name='voter_question')



    def __str__(self):
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='author_answer') #Question 삭제 시 Question과 연관된 것들 다 삭제 (답변에 연관된 질문이 삭제되면 답변도 모두 삭제 )
    content = models.TextField() # 글자 수 제한 없는 컬럼
    create_date = models.DateTimeField() # 날짜 + 시간
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # author필드 추가: 글쓴이
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    #입력 필드에 null허용하기
    # author=models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    #수정일시 추가
    modify_date = models.DateTimeField(null=True, blank=True)
    # modify_date = models.DateTimeField(null=True, blank=True)

    #추천
    voter = models.ManyToManyField(User, related_name='voter_answer')


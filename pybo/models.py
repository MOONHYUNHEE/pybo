from django.db import models

# Create your models here.
# 질문 클래스(테이블)  생성 : subject, content, create_date (장고 - 키 값 넣지 않고 생성 시 자동으로 키 값 생성됨)
class Question(models.Model):
    subject = models.CharField(max_length=200) # max_length = 글자수 제한
    content = models.TextField() # 글자수 제한 없는 컬럼
    create_date = models.DateTimeField() # 날짜 + 시간

    def __str__(self):
        return self.subject




class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #Question 삭제 시 Question과 연관된 것들 다 삭제 (답변에 연관된 질문이 삭제되면 답변도 모두 삭제 )
    content = models.TextField() # 글자 수 제한 없는 컬럼
    create_date = models.DateTimeField() # 날짜 + 시간
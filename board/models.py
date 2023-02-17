from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Board(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    subject = models.CharField(max_length=200)# 글자수 제한
    content = models.TextField() #글자수 제한이 없는 경우
    create_date = models.DateTimeField() #날짜 + 시간
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author_board')   #회원테이블에 사용자 정보가 삭제 되면 Question 테이블 질문도 모두 삭제
    modify_date = models.DateTimeField(blank=True, null=True) ## 데이터 베이스에서 null 허용, form.is_valid() 입력값 검증시 값이 없어도 된다. blank=True

    class Meta:
        managed = False
        db_table = 'board'

    def __str__(self):
        return self.subject
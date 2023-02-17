'''
파일명 : forms.py
설 명 :
생성일 : 2023-02-15
생성자 : user
since 2023.01.09 Copyright (C) by KandJang All right reserved.
'''

from django import forms
from board.models import Board


class BoardForm(forms.ModelForm):
    class Meta:
        model = Board #사용모델
        fields=['subject','content']

        labels ={    #subject->제목으로 변경
            'subject': '제목',
            'content': '내용',
        }
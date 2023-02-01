from django.contrib import admin

from .models import Question
# Register your models here.

#Question을 admin에 등록  : import 후 아래와 같이 기재
class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['subject']
admin.site.register(Question, QuestionAdmin)

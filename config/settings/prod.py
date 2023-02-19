'''
파일명: prod.py
설명:
생성일 : 2023-02-19
생성자: judge
since 2023.01.09 Copyright (c) by KandJang All right reserved.
'''
from .base import BASE_DIR
from .prod import *
import environ
ALLOWED_HOSTS = ['43.200.51.48'] #AWS 고정 IP
STATIC_ROOT = BASE_DIR / 'static/'
#이유는 STATIC_ROOT가 설정된 경우 STATICFILES_DIRS 리스트에 STATIC_ROOT와 동일한 디렉터리가 포함되어 있으면
# 서버 실행 시 다음과 같은 오류가 발생
STATICFILES_DIRS = []

env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

DATABASES = {
    'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': env('DB_NAME'),
		'USER': env('DB_USER'),
		'PASSWORD': env('DB_PASSWORD'),
		'HOST': env('DB_HOST'),
		'PORT': '3306',
    }
}
import os
from rest_framework import serializers

def validate_image(value):
    # ext에 이미지의 확장자명을 담기
    ext = os.path.splitext(value.name)[1][1:]
    # 확장자명을 소문자로 통일
    ext = ext.lower()
    # 확장자명이 png이면 에러
    if ext in ['png']:
      raise serializers.ValidationError('PNG 형식은 지원하지 않습니다.')
from rest_framework import serializers
from .models import Post, Comment
import os

class PostSerializer(serializers.ModelSerializer):

  class Meta:
    model = Post
    fields = "__all__"

    # 특정 필드 갖고오기
    # fields = ['writer', 'content']
    
    # 특정 필드 제외하기
    # exclude = ['category']

    # 읽기 전용 필드 지정
    # read_only_fields = ['writer']
  
  def validate_image(self, value):
    # ext에 이미지의 확장자명을 담기
    ext = os.path.splitext(value.name)[1][1:]
    # 확장자명을 소문자로 통일
    ext = ext.lower()
    # 확장자명이 png이면 에러
    if ext in ['png']:
      raise serializers.ValidationError(f'Unsupported file extension: .{ext}.')

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['writer', 'content',]


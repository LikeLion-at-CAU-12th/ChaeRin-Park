from rest_framework import serializers
from .models import Post, Comment
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

class PostSerializer(serializers.ModelSerializer):

  class Meta:
    model = Post
    exclude = ['thumnail_url']

    # 특정 필드 갖고오기
    # fields = ['writer', 'content']
    
    # 특정 필드 제외하기
    # exclude = ['category']

    # 읽기 전용 필드 지정
    # read_only_fields = ['writer']
    
  def validate_image(self, value):
    print('hello')
    # ext에 이미지의 확장자명을 담기
    ext = os.path.splitext(value.thumnail)[1][1:]
    # 확장자명을 소문자로 통일
    ext = ext.lower()
    # 확장자명이 png이면 에러
    if ext in ['png']:
      raise serializers.ValidationError(f'Unsupported file extension: .{ext}.')
    return value
  
  def create(self, validated_data):
    thumnail = validated_data.pop('thumnail')
    file_name = default_storage.save(thumnail.name, ContentFile(thumnail.read()))
    thumnail_url = default_storage.url(file_name)

    instance = Post.objects.create(thumnail_url=thumnail_url, **validated_data)
    return instance

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['writer', 'content',]


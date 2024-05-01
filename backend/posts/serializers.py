from rest_framework import serializers
from .models import Post, Comment

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

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = ['writer', 'content',]
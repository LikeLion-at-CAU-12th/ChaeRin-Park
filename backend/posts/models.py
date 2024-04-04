from django.db import models

## 추상 클래스 정의
class BaseModel(models.Model):
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        abstract = True

# 게시글 테이블
class Post(BaseModel):

    CHOICES = (
        ('DIARY', '일기'),
        ('STUDY', '공부'),
        ('ETC', '기타')
    )

    post_id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name="제목", max_length=20)
    content = models.TextField(verbose_name="내용")
    writer = models.CharField(verbose_name="작성자", max_length=10)
    category = models.CharField(choices=CHOICES, max_length=20)

# 댓글 테이블
class Comment(BaseModel):

    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, verbose_name="게시글", on_delete=models.CASCADE)
    writer = models.CharField(verbose_name="작성자", max_length=10)
    content = models.TextField(verbose_name="내용")

# 해시태그 테이블
class Hashtag(BaseModel):

    tag_id = models.AutoField(primary_key=True)
    content = models.CharField(verbose_name="해시태그", max_length=20)
    post = models.ManyToManyField(Post, through='HashtagPosts')

# 해시태그와 게시글의 중간 테이블
class HashtagPosts(BaseModel):
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
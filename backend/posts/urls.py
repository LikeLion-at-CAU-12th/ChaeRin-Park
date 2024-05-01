from django.urls import path
from posts.views import *

urlpatterns = [
    #path('', post_list, name="post_list"),  #post 전체 조회
    #path('<int:id>/', post_detail, name="post_detail"), # Post 단일 조회
    #path('<int:id>/comment/', comment_list, name="comment_list"), # post의 comment 전체 조회
    #path('recent/', recent_post_list, name="recent_post_list")
    path('', PostList.as_view()),
    path('<int:id>', PostDetail.as_view()),
    path('<int:id>/comments', CommentList.as_view())
]
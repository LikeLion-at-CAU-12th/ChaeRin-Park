from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
from posts.models import *
import json
from datetime import datetime, timedelta, date # 날짜


# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello lielion-12th!"
        })
    
def index(request):
    return render(request, 'index.html')


@require_http_methods(["POST", "GET"])
def post_list(request):
    
    if request.method == "POST":
    
	      # 새로운 데이터를 DB에 생성
        new_post = Post.objects.create(
            writer = request.POST.get('writer'),
            title = request.POST.get('title'),
            content = request.POST.get('content'),
            category = request.POST.get('category'),
            imgfile = request.FILES.get('imgfile'),
        )
        
    
	      # Response에서 보일 데이터 내용을 Json 형태로 만들어줌
        new_post_json = {
            "id": new_post.post_id,
            "writer": new_post.writer,
            "title" : new_post.title,
            "content": new_post.content,
            "category": new_post.category,
            'image': str(new_post.imgfile),
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 생성 성공',
            'data': new_post_json,
        })
    
    if request.method == "GET":
        post_all = Post.objects.all()
    
				# 각 데이터를 Json 형식으로 변환하여 리스트에 저장
        post_json_all = []
        
        for post in post_all:
            post_json = {
                "id": post.post_id,
                "title" : post.title,
                "writer": post.writer,
                "category": post.category,
            }
            post_json_all.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '게시글 목록 조회 성공',
            'data': post_json_all,
        })
    
@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):
		# 요청 메소드가 GET일 때는 게시글을 조회하는 View가 동작하도록 함
    if request.method == "GET":
        post = get_object_or_404(Post, pk=id)
        
        post_json = {
            "id": post.post_id,
            "writer": post.writer,
            "title" : post.title,
            "content": post.content,
            "category": post.category,
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 조회 성공',
            'data': post_json
        })
    
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        
        update_post = get_object_or_404(Post, pk=id)

        update_post.title = body['title']
        update_post.content = body['content']
        update_post.category = body['category']
        
        update_post.save()

        update_post_json = {
            "id": update_post.post_id,
            "writer": update_post.writer,
            "title" : update_post.title,
            "content": update_post.content,
            "category": update_post.category,
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 수정 성공',
            'data': update_post_json
        })
    
    if request.method == "DELETE":
        delete_post = get_object_or_404(Post, pk=id)
        delete_post.delete()

        return JsonResponse({
                'status': 200,
                'message': '게시글 삭제 성공',
                'data': None
        })
    

# 댓글 기능
@require_http_methods(["POST", "GET"])
def comment_list(request, id):
    
    post_page = get_object_or_404(Post, pk=id)

    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
    
	      # 새로운 데이터를 DB에 생성
        new_comment = Comment.objects.create(
            post = post_page,
            writer = body['writer'],
            content = body['content'],
        )
    
	      # Response에서 보일 데이터 내용을 Json 형태로 만들어줌
        new_comment_json = {
            "id" : new_comment.comment_id,
            "writer": new_comment.writer,
            "content": new_comment.content,
        }

        return JsonResponse({
            'status': 200,
            'message': '댓글 생성 성공',
            'data': new_comment_json
        })
    
    if request.method == "GET":
        comment_all = Comment.objects.filter(post_id = id)
    
				# 각 데이터를 Json 형식으로 변환하여 리스트에 저장
        comment_json_all = []
        
        for comment in comment_all:
            comment_json = {
                "id" : comment.comment_id,
                "writer": comment.writer,
                "content": comment.content,
            }

            comment_json_all.append(comment_json)

        return JsonResponse({
            'status': 200,
            'message': '댓글 목록 조회 성공',
            'data': comment_json_all
        })
    
# 최근 게시물 기능
@require_http_methods(["GET"]) 
def recent_post_list(request):
    if request.method == "GET":

        post_all = Post.objects.filter(created_at__range=[date(2024, 4, 4), date(2024, 4, 10)]).order_by('-pk')

        post_json_all = []
        
        for post in post_all:
            post_json = {
                "id": post.post_id,
                "title" : post.title,
                "writer": post.writer,
                "category": post.category,
                "created_at": post.created_at,
            }
            post_json_all.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '게시글 목록 조회 성공',
            'data': post_json_all
        })
    




from .serializers import *

# APIView를 사용하기 위해 import
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

# class PostList(APIView):
#     def post(self, request, format=None):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     
#     def get(self, request, format=None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
# 
#class PostDetail(APIView):
#    def get(self, request, id):
#        post = get_object_or_404(Post, post_id=id)
#        serializer = PostSerializer(post)
#        return Response(serializer.data)
#    
#    def put(self, request, id):
#        post = get_object_or_404(Post, post_id=id)
#        serializer = PostSerializer(post, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data) 
#        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#    
#    def delete(self,request,id):
#        post = get_object_or_404(Post, post_id=id)
#        post.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
    
# 스탠다드 과제
class CommentList(APIView):
    def post(self, request, id, format=None):
        post_page = get_object_or_404(Post, pk=id)
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post = post_page)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id, format=None):
        comments = Comment.objects.filter(post_id = id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

# 챌린지 과제
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
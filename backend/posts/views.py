from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
from posts.models import *
import json

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
        body = json.loads(request.body.decode('utf-8'))
    
	      # 새로운 데이터를 DB에 생성
        new_post = Post.objects.create(
            writer = body['writer'],
            title = body['title'],
            content = body['content'],
            category = body['category']
        )
    
	      # Response에서 보일 데이터 내용을 Json 형태로 만들어줌
        new_post_json = {
            "id": new_post.post_id,
            "writer": new_post.writer,
            "title" : new_post.title,
            "content": new_post.content,
            "category": new_post.category
        }

        return JsonResponse({
            'status': 200,
            'message': '게시글 생성 성공',
            'data': new_post_json
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
                "category": post.category
            }
            post_json_all.append(post_json)

        return JsonResponse({
            'status': 200,
            'message': '게시글 목록 조회 성공',
            'data': post_json_all
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
            'message': '게시글 목록 조회 성공',
            'data': comment_json_all
        })
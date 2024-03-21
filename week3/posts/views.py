from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello lielion-12th!"
        })
    
def codeReviewer(request):
    if request.method == "GET":
        return JsonResponse({
	'status' : 200,
	'success' : True,
	'message' : '메시지 전달 성공!',
	'data' : [
		{
			"name" : "박채린",
			"age" : 21,
			"major" : "CSE"
		},
		{
			"name" : "이강록",
			"age" : 22,
			"major" : "CSE"
		}
	]
},
json_dumps_params={'ensure_ascii': False})
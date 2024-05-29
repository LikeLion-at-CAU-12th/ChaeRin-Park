from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from pathlib import Path
import os, json
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from json import JSONDecodeError
from django.http import JsonResponse
import requests

# 9주차 스탠다드 과제
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from dj_rest_auth.registration.serializers import SocialLoginSerializer
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google import views as google_view

# BASE_URL 정의
BASE_URL = "http://127.0.0.1:8000/"

# Create your views here.
class RegisterView(APIView):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save(request)
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": serializer.data,
                    "message": "register success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class AuthView(APIView):
    def post(self, request):
        serializer = AuthSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            access_token = serializer.validated_data["access_token"]
            refresh_token = serializer.validated_data["refresh_token"]
            res = Response(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK,
            )
            res.set_cookie("access-token", access_token, httponly=True)
            res.set_cookie("refresh-token", refresh_token, httponly=True)
            return res
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"massage": "로그아웃되었습니다"}, status=status.HTTP_200_OK)
    
BASE_DIR = Path(__file__).resolve().parent.parent
secret_file = os.path.join(BASE_DIR, "secrets.json")

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)

GOOGLE_SCOPE_USERINFO = get_secret("GOOGLE_SCOPE_USERINFO")
GOOGLE_REDIRECT = get_secret("GOOGLE_REDIRECT")
GOOGLE_CALLBACK_URI = get_secret("GOOGLE_CALLBACK_URI")
GOOGLE_CLIENT_ID = get_secret("GOOGLE_CLIENT_ID")
GOOGLE_SECRET = get_secret("GOOGLE_SECRET")

# 프론트엔드 측에서 접근하는 엔드포인트이자 백엔드가 구글에서 인가코드를 받아오는 엔드포인트
def google_login(request):
   scope = GOOGLE_SCOPE_USERINFO        # + "https://www.googleapis.com/auth/drive.readonly" 등 scope 설정 후 자율적으로 추가
   return redirect(f"{GOOGLE_REDIRECT}?client_id={GOOGLE_CLIENT_ID}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")

def google_callback(request):
    code = request.GET.get("code")      # Query String 으로 넘어옴
    # 인가 코드를 넘겨주고 엑세스 토큰 받아오기
    
    # 받은 인가 코드로 구글에 엑세스 토큰을 요청
    token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={GOOGLE_CLIENT_ID}&client_secret={GOOGLE_SECRET}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}")
    
    # 얘를 json화
    token_req_json = token_req.json()
    error = token_req_json.get("error")

    # 에러 발생 시 종료
    if error is not None:
        raise JSONDecodeError(error)

    # 성공 시 엑세스 토큰을 가지고 오기
    google_access_token = token_req_json.get('access_token')

    # 가져온 엑세스 토큰으로 이메일 값을 구글에 요청
    email_response = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={google_access_token}")
    res_status = email_response.status_code

    # 200 status가 아니면(에러 발생 시) 400 status 반환
    if res_status != 200:
        return JsonResponse({'status': 400,'message': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 성공 시 이 때부터 이메일을 잘 지니고 있음
    email_res_json = email_response.json()
    email = email_res_json.get('email')

    try:
        # 해당 이메일의 유저가 존재하는지 탐색
        user = User.objects.get(email=email)

        # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 존재하는지 탐색
        social_user = SocialAccount.objects.get(user=user)

        # socialaccount 테이블에 존재하기는 하지만, 구글 계정이 아니라면 에러
        if social_user.provider != "google":
            return JsonResponse(
                {"message": "소셜이 일치하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 이미 구글로 제대로 가입되어 있는 유저라면 로그인, jwt 발급
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}account/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 문제가 생기면 에러
        if accept_status != 200:
            return JsonResponse({"message": "구글로그인에 실패했습니다."}, status=accept_status)

        user, created = User.objects.get_or_create(email=email)
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)

        # accept_json = accept.json()
        # accept_json.pop("user", None)
        return Response(
            {"refresh": str(refresh_token), "access": str(access_token)},
            status=status.HTTP_200_OK,
        )

    # 유저 테이블에 유저가 아예 없으면 새로 회원가입하고 jwt 발급
    except User.DoesNotExist:
        data = {"access_token": access_token, "code": code}
        accept = requests.post(f"{BASE_URL}account/google/login/finish/", data=data)
        accept_status = accept.status_code

        # 문제 발생 시 에러
        if accept_status != 200:
            return JsonResponse({"message": "구글 회원가입에 실패했습니다."}, status=accept_status)

        user, created = User.objects.get_or_create(email=email)
        access_token = AccessToken.for_user(user)
        refresh_token = RefreshToken.for_user(user)
        # accept_json = accept.json()
        # accept_json.pop("user", None)

        return Response(
            {"refresh": str(refresh_token), "access": str(access_token)},
            status=status.HTTP_201_CREATED,
        )
    
    # 유저 테이블에는 존재하지만 Social account 테이블에는 없을 때(일반 회원)
    except SocialAccount.DoesNotExist:
        return JsonResponse(
            {"message": "소셜로그인 유저가 아닙니다."},
            status=status.HTTP_400_BAD_REQUEST,
        )


class GoogleLogin(SocialLoginView):
    adapter_class = google_view.GoogleOAuth2Adapter
    callback_url = GOOGLE_CALLBACK_URI
    client_class = OAuth2Client
    serializer_class = SocialLoginSerializer
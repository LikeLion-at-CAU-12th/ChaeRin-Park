from rest_framework_simplejwt.serializers import RefreshToken
from rest_framework import serializers
from .models import User
from allauth.socialaccount.models import SocialAccount

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['password', 'username', 'email']

    def save(self, request):

        user = User.objects.create(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )

        # password 암호화
        user.set_password(self.validated_data['password'])
        user.save()

        return user
    
    def validate(self, data):
        email = data.get('email', None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidtionError('email already exists')
        
        return data
    
class AuthSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get("username", None)
        password = data.get("password", None)

        user = User.get_user_or_none_by_username(username=username)

        if user is None:
            raise serializers.ValidationError("user account not exist")
        else:
            if not user.check_password(raw_password=password):
                raise serializers.ValidationError("wrong password")
            
        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        return data
    
    # is None과 ==None의 차이

class OAuthSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ["email"]

    # 유저의 이메일이 있는지 없는지 확인
    def validate(self, data):
        email = data.get("email", None)
        
        user = User.get_user_or_none_by_email(email=email)
        # FK로 연결되어 있는 socialaccount 테이블에서 해당 이메일의 유저가 존재하는지 탐색
        social_user = SocialAccount.objects.get(user=user)

        if user is None:
            raise serializers.ValidationError("user account not exists")

        token = RefreshToken.for_user(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        # 토큰 발급해서 넘겨주기
        data = {
            "user": user,
            "refresh_token": refresh_token,
            "access_token": access_token,
        }

        # socialaccount 테이블에 존재하기는 하지만, 구글 계정이 아니라면 에러
        if social_user.provider == "google":
            return data
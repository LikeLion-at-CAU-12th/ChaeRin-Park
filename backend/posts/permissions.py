from rest_framework.permissions import BasePermission
from rest_framework .permissions import SAFE_METHODS

class KeyCheck(BasePermission):
	def has_permission(self, request, view):
		secret_key = request.META.get('HTTP_CUSTOM_HEADER', None)
		if secret_key == 'cherrynniii':
			return True
		return False
	
class OnlyWriterManage(KeyCheck):
	# 인증된 유저에 한해, 목록조회/포스팅등록 허용
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.is_authenticated

    # 작성자에 한해, Record에 대한 수정/삭제 허용
    def has_boject_permission(self, request, view, obj):
        # 안전한 조회 요청(GET, HEAD, OPTIONS) 에 대해서는 인증여부에 상관없이 허용
        if request.method in SAFE_METHODS:
            return True
        
        # PUT, DELETE 요청에 대해, 작성자일 경우에만 요청 허용
        return obj.author == request.user
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status


class GenericAPIException(APIException):
    def __init__(self, status_code, detail=None, code=None):
        self.status_code=status_code
        super().__init__(detail=detail, code=code)
        
class IsAdmin(BasePermission):
    """
    admin 사용자는 모든request 가능,
    비로그인, 로그인한 사람은 조회만 가능
    """

    SAFE_METHODS = ('GET', )
    message = '접근 권한이 없습니다.'

    def has_permission(self, request, view):
        user = request.user
        
        if request.method in self.SAFE_METHODS:
            return True

        if not user.is_admin:
            response = {
                'detail': "관리자만 접근이 가능합니다."
            }
            raise GenericAPIException(status_code=status.HTTP_403_FORBIDDEN, detail=response)
        
        if user.is_admin:
            return True
        
        if (user.is_anonymous or user.is_authenticated) and request.method in self.SAFE_METHODS:
            return True

        return False
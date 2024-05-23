from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from .models import *

class User(AbstractUser):
    email = models.CharField(verbose_name="email", max_length=30)

    deleted_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(null=True, blank=True)
    restore = models.CharField(max_length=20, null=True, blank=True)

    @staticmethod
    def get_user_or_none_by_username(username):
        try:
            return User.objects.get(username=username)
        except Exception:
            return None
    
    # soft delete 함수
    def softDelete(self, restore, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.restore = restore
        self.is_deleted = True
        self.save()

    # 삭제를 복구하는 함수
    def restore(self, restore):
        if self.restore == restore:
            self.deleted_at = None
            self.is_deleted = False
            self.save()
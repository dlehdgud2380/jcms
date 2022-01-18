from django.db import models

# Create your models here.

class Dashboard(models.Model):
    """
    간단한 컨테이너 대쉬보드를 구성하는 모델을 작성
    """
    container_name = models.TextField()
    container_status = models.BooleanField()
    container_id = models.TextField()
    request_client_name = models.CharField(max_length=50)

class User(models.Model):
    """
    유저리스트
    """
    name = models.TextField()
    admin = models.BooleanField()
    container_id = models.TextField()
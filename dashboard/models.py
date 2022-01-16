from django.db import models

# Create your models here.

# 간단한 컨테이너 대쉬보드를 구성하는 모델을 작성
class Dashboard(models.Model):
    container_name = models.TextField()
    container_status = models.BooleanField()
    container_id = models.TextField()
    request_client_name = models.CharField(max_length=50)
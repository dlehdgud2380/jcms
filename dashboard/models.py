from django.db import models

# Create your models here.

class Container(models.Model):
    """
    간단한 컨테이너 대쉬보드를 구성하는 모델을 작성
    * 컨테이너명
    * 컨테이너 상태
    * 컨테이너 포트
    * 컨테이너 IP
    * 컨테이너 쥬피터 토큰
    * 컨테이너 생성 요청자
    """
    name = models.CharField(max_length=50, null=True)
    ctnId = models.TextField(null=True)
    health = models.BooleanField()
    port = models.CharField(max_length=10, null=True)
    ip = models.TextField(max_length=50, null=True)
    jupyterToken = models.TextField(null=True)
    clientName = models.CharField(max_length=50)

    def __str__(self) -> str:
        """
        id 대신 제목을 표시 해주는 기능
        """
        return self.name

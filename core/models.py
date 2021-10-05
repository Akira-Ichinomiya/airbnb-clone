from django.db import models
from . import managers

# Create your models here.
class TimeStampedModel(models.Model):
    """
    Time Stamped Model
    """

    created = models.DateTimeField(
        auto_now_add=True, blank=True, null=True
    )  # 생성된 날짜 기록
    modified = models.DateTimeField(auto_now=True, blank=True, null=True)  # 변경 시 최신화 해줌
    objects = managers.CustomModelManager()

    class Meta:  # 추상형인지의 여부를 이곳에 표시할 수 있음
        abstract = True

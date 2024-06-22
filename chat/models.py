from django.db import models
from common.models import CommonModel
# Create your models here.


class BaseFirstChat(CommonModel):
    nickname = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
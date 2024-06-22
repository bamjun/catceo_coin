from django.db import models
from common.models import CommonModel
import pytz

# Create your models here.


class BaseFirstChat(CommonModel):
    nickname = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.nickname

    def get_ny_time(self):
        return self.time.astimezone(pytz.timezone('America/New_York'))

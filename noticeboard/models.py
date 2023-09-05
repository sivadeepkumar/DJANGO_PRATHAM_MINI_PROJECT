from django.db import models
from django.contrib.auth.models import User

class NoticeBoard(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    notice =models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.message
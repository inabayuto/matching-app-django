from django.db import models
from django.conf import settings

class DM(models.Model):
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_dms',
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_dms',
    )

    message = models.TextField(verbose_name='メッセージ', max_length=1000)
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)


    def __str__(self):
        return f'{self.sender.username} send to {self.receiver.username}'
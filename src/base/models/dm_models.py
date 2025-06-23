from django.db import models
from django.conf import settings

class DM(models.Model):
    """
    ユーザー同士のダイレクトメッセージを管理するモデル。
    sender（送信者）とreceiver（受信者）のユーザー間のメッセージを1レコードで表現。
    messageでメッセージの内容を管理。
    created_atでメッセージの作成日時を管理。
    """
    # 送信者
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_dms',
    )
    # 受信者
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_dms',
    )
    # メッセージ
    message = models.TextField(verbose_name='メッセージ', max_length=1000)
    # メッセージの作成日時
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True)


    def __str__(self):
        """
        管理画面やシェルでの表示用。
        例: "userA send to userB"
        """
        return f'{self.sender.username} send to {self.receiver.username}'
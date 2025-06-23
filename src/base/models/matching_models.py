from django.db import models
from django.conf import settings

class Matching(models.Model):
    """
    ユーザー同士のマッチング関係を管理するモデル。
    approaching（アプローチした側）とapproached（アプローチされた側）のユーザー間の関係を1レコードで表現。
    approvedでマッチング成立可否を管理。
    """
    # アプローチしたユーザー（送信者）
    approaching = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='approaching_user',
    )
    # アプローチされたユーザー（受信者）
    approached = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='approached_user',
    )
    # マッチングが承認されたかどうか
    approved = models.BooleanField(verbose_name='マッチング許可', default=False) # マッチング許可の有無
    # レコード作成日時（自動記録）
    created_at = models.DateTimeField(verbose_name='登録日時', auto_now_add=True) # 登録日時

    class Meta:
        # approaching, approached の組み合わせは一意（重複禁止）
        unique_together = (('approaching', 'approached'))

    def __str__(self):
        """
        管理画面やシェルでの表示用。
        例: "userA like to userB"
        """
        return f'{self.approaching.username} like to {self.approached.username}'
    
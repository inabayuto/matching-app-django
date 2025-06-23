from django.db import models
from django.conf import settings
import uuid
from datetime import timedelta
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail



class UserActivateTokensManager(models.Manager):

    def activate_user_by_token(self, activate_token):
        user_activate_token = self.filter(
            activate_token=activate_token,
            expired_at__gte=timezone.now() # __gte = greater than equal
        ).first()
        if hasattr(user_activate_token, 'user'):
            user = user_activate_token.user
            user.is_active = True
            user.save()
            return user

class UserActivateTokens(models.Model):

    token_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activate_token = models.UUIDField(default=uuid.uuid4)
    expired_at = models.DateTimeField()

    objects = UserActivateTokensManager()

    def is_expired(self):
        return self.expired_at < timezone.now()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def publish_activate_token(sender, instance, **kwargs):
    if not instance.is_active:
        user_activate_token = UserActivateTokens.objects.create(
            user=instance,
            expired_at=timezone.now()+timedelta(days=settings.ACTIVATION_EXPIRED_DAYS),
        )
        subject = 'Please Activate Your Account'
        message = f'URLにアクセスして決済を完了してください。\n {settings.MY_URL}/api/users/{user_activate_token.token_id}/payment/'
    if instance.is_active:
        subject = 'Activated! Your Account!'
        message = 'ユーザーが使用できるようになりました'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [
        instance.email,
    ]
    send_mail(subject, message, from_email, recipient_list)  
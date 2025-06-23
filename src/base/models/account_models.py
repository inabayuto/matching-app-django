from django.db import models
from django.contrib.auth.models import BaseUserManager,  AbstractBaseUser,  PermissionsMixin
import uuid
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserManager(BaseUserManager):
    """
    カスタムユーザーモデル用のマネージャークラス。
    通常ユーザーとスーパーユーザーの作成ロジックを集約。
    DjangoのBaseUserManagerを継承し、email認証に対応。
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        一般ユーザーを作成するメソッド。

        Args:
            email (str): ユーザーのメールアドレス（必須）
            password (str, optional): パスワード。デフォルトはNone。
            **extra_fields: その他追加フィールド（例：first_name, last_name など）

        Returns:
            User: 作成されたユーザーインスタンス

        Raises:
            ValueError: emailが未指定の場合に発生
        """
        # メールアドレスが未入力の場合は例外を投げる
        if not email:
            raise ValueError('Email is required')
        # emailを正規化し、追加フィールドとともにユーザーインスタンスを生成
        user =  self.model(email=self.normalize_email(email), **extra_fields)
        # パスワードをハッシュ化してセット
        user.set_password(password)
        # データベースに保存
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password):
        """
        スーパーユーザー（管理者）を作成するメソッド。
        is_staff, is_superuserをTrueに設定。

        Args:
            email (str): 管理者のメールアドレス
            password (str): パスワード

        Returns:
            User: 作成されたスーパーユーザーインスタンス
        """
        # create_userを使ってベースユーザーを作成
        user =  self.create_user(email, password)
        # 管理者権限を付与
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True # スーパーユーザーは作成時に有効化
        # データベースに保存
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    カスタムユーザーモデル。
    AbstractBaseUserを継承し、Djangoの認証システムをカスタマイズ。
    PermissionsMixinを継承し、権限管理をサポート。
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # ユーザーID
    email = models.EmailField(max_length=255, unique=True) # メールアドレス
    username = models.CharField(max_length=255, unique=True) # ユーザー名
    is_active =  models.BooleanField(default=False) # ユーザーの有効化状態
    is_staff =  models.BooleanField(default=False) # スタッフ権限

    objects =  UserManager()

    USERNAME_FIELD = 'email'

    # ユーザーのメールアドレスを返す
    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    ユーザーのプロフィール情報を管理するモデル。
    Userモデルと1対1の関係を持ち、ユーザーの詳細情報を保持。
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE, related_name='profile') # ユーザーと1対1の関係を持つ
    is_kyc = models.BooleanField('本人確認', default=False) # 本人確認の有無
    nickname = models.CharField('ニックネーム', max_length=255, blank=True, null=True) # ニックネーム
    created_at = models.DateTimeField('登録日時', auto_now_add=True) # 登録日時
    updated_at = models.DateTimeField('更新日時', auto_now=True, blank=True, null=True) # 更新日時
    age = models.PositiveBigIntegerField('年齢', validators=[MinValueValidator(18), MaxValueValidator(100)], blank=True, null=True) # 年齢
    SEX = [
        ('male', '男性'),
        ('female', '女性'),
    ]
    sex = models.CharField('性別', max_length=10, choices=SEX, blank=True, null=True) # 性別
    introduction = models.TextField('自己紹介', blank=True, null=True) # 自己紹介

    # ニックネームが存在する場合はニックネームを返し、存在しない場合はユーザー名を返す
    def __str__(self):
        return self.nickname if self.nickname else str(self.user)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_on_user_create(sender, instance=None, created=False, **kwargs):
    """
    Userモデルのインスタンスが作成された時（created=True）、
    関連するProfileモデルのインスタンスも自動的に作成する。
    """
    if created:
        Profile.objects.create(user=instance)
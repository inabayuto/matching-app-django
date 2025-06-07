from django.db import models
from django.contrib.auth.models import BaseUserManager,  AbstractBaseUser,  PermissionsMixin
import uuid

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
        # データベースに保存
        user.save(using=self._db)
        return user

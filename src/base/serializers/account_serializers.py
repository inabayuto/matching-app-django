# serializers.py: Django REST frameworkのシリアライザ定義ファイル
# シリアライザは、モデルインスタンスとJSON等のデータ変換・バリデーションを担う。

from rest_framework import serializers
from django.contrib.auth import get_user_model
from base.models import Profile

class UserSerializer(serializers.ModelSerializer):
    """
    ユーザーモデル用のシリアライザ
    - ユーザー作成時はパスワードをwrite_onlyにし、8文字以上を要求
    - create/updateでパスワードのハッシュ化も行う
    """
    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        """
        新規ユーザー作成時の処理
        パスワードはハッシュ化されて保存される
        """
        # UserManagerのcreate_userを利用してユーザー作成
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """
        既存ユーザー情報の更新時の処理
        パスワード更新時はハッシュ化して保存
        その他のフィールドは通常通り更新
        """
        # validated_dataの各フィールドを更新
        for key, value in validated_data.items():
            if key == 'password':
                # パスワードはハッシュ化して保存
                instance.set_password(value)
            else:
                setattr(instance, key, value)
        instance.save()
        return instance

class ProfileSerializer(serializers.ModelSerializer):
    """
    プロフィールモデル用のシリアライザ
    - 日時フィールドはフォーマット指定で出力
    - userフィールドはread_only
    """
    # 日時フィールドはフォーマット指定で出力
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = Profile
        fields = ('id', 'user', 'is_kyc', 'nickname', 'created_at', 'updated_at', 'age', 'sex', 'introduction')
        extra_kwargs = {'user': {'read_only': True}}
        

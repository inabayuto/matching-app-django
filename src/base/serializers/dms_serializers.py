# ダイレクトメッセージ関連モデルのシリアライザ定義
# シリアライザは、モデルインスタンスとJSON等のデータ変換・バリデーションを担う

from base.models import DM
from .matching_serializers import MatchingFilter
from rest_framework import serializers

class DirectMessageSerializer(serializers.ModelSerializer):
    """
    DirectMessageモデル用のシリアライザ
    - created_atはフォーマット指定で出力
    - receiverはMatchingFilterでマッチング済みユーザーのみ選択可能
    - senderはread_only
    """
    # 登録日時をフォーマット指定で出力
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    # マッチング済みユーザーのみ選択可能なカスタムフィルタ
    receiver = MatchingFilter()

    class Meta:
        model = DM
        fields = ('id', 'sender', 'receiver', 'message', 'created_at')
        extra_kwargs = {'sender': {'read_only': True}}
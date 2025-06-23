# ダイレクトメッセージ関連モデルのシリアライザ定義
# シリアライザは、モデルインスタンスとJSON等のデータ変換・バリデーションを担う

from django.contrib.auth import get_user_model
from rest_framework import serializers
from base.models import DM, Matching
from django.db.models import Q

class DirectMessageSerializer(serializers.ModelSerializer):
    """
    DirectMessageモデル用のシリアライザ
    - receiverの選択肢をマッチング済みのユーザーに動的に絞り込む
    """
    # receiverフィールドをPrimaryKeyRelatedFieldとして定義
    receiver = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())
    # 登録日時をフォーマット指定で出力
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # コンテキストからリクエストを取得
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            # ログインユーザーとマッチング済みのユーザーを取得
            lovers = Matching.objects.filter(
                Q(approaching=request.user, approved=True) |
                Q(approached=request.user, approved=True)
            )
            # マッチング相手のIDリストを作成
            lover_ids = [m.approached.id if m.approaching == request.user else m.approaching.id for m in lovers]
            # receiverフィールドの選択肢を絞り込む
            self.fields['receiver'].queryset = get_user_model().objects.filter(id__in=lover_ids)

    class Meta:
        model = DM
        fields = ('id', 'sender', 'receiver', 'message', 'created_at')
        extra_kwargs = {
            'sender': {'read_only': True},
        }
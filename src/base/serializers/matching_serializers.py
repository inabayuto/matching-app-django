# マッチング関連モデルのシリアライザ定義
# シリアライザは、モデルインスタンスとJSON等のデータ変換・バリデーションを担う

from rest_framework import serializers
from base.models import Matching
from django.db.models import Q
from django.contrib.auth import get_user_model

class MatchingSerializer(serializers.ModelSerializer):
    """
    Matchingモデル用のシリアライザ
    - created_atはフォーマット指定で出力
    - approachingはread_only
    """
    # 登録日時をフォーマット指定で出力
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = Matching
        fields = ('id', 'approaching', 'approached', 'approved', 'created_at')
        extra_kwargs = {'approaching': {'read_only': True}}


class MatchingFilter(serializers.PrimaryKeyRelatedField):
    """
    マッチング済みユーザーのみを絞り込むためのカスタムフィルタ
    - request.userが関与するapprovedなMatchingのみを抽出
    - そのユーザーIDリストでUserクエリセットを返す
    """
    def get_queryset(self):
        # リクエストユーザーを取得
        request = self.context['request']
        # マッチング済み（approved=True）かつ自分が関与するMatchingを抽出
        lovers =  Matching.objects.filter(
            Q(approaching=request.user) | Q(approached=request.user),
            approved=True,
        )
        # 関与ユーザーのIDリストを作成
        list_lover = []
        for lover in lovers:
            list_lover.append(lover.approaching.id)
        # IDリストに該当するユーザーのみ返す
        queryset = get_user_model().objects.filter(id__in=list_lover)
        return queryset
        
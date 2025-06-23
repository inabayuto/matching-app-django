from base.models import DM
from base.serializers import DirectMessageSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet


class DirectMessageViewSet(ModelViewSet):
    """
    ダイレクトメッセージ情報取得用のビュー。
    ダイレクトメッセージ情報を取得する。
    """
    queryset = DM.objects.all()
    serializer_class = DirectMessageSerializer

    def get_queryset(self):
        """
        ダイレクトメッセージ情報を取得する。
        """
        return self.queryset.filter(sender=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Delete DM is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
class InboxListView(ReadOnlyModelViewSet):
    """
    受信メッセージ一覧取得用のビュー。
    受信メッセージ一覧を取得する。
    """
    queryset = DM.objects.all()
    serializer_class = DirectMessageSerializer

    def get_queryset(self):
        return self.queryset.filter(receiver=self.request.user)

    

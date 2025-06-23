from rest_framework.exceptions import ValidationError
from base.models import Matching
from base.serializers import MatchingSerializer
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status


class MatchingViewSet(ModelViewSet):
    """
    マッチング情報取得用のビュー。
    マッチング情報を取得する。
    """
    queryset = Matching.objects.all()
    serializer_class = MatchingSerializer

    def get_queryset(self):
        """
        マッチング情報を取得する。
        """
        return self.queryset.filter(Q(approaching=self.request.user) | Q(approached=self.request.user))

    def perform_create(self, serializer):
        """
        マッチング情報を作成する。
        """
        try:
            serializer.save(approaching=self.request.user)
        except ValidationError:
            raise ValidationError("User cannot approach unique user a number of times")

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Delete is not allowed !'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

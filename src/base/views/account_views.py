from rest_framework.viewsets import ModelViewSet
from base.models import Profile
from base.serializers import ProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from base.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUserView(CreateAPIView):
    """
    ユーザー作成用のビュー。
    ユーザーの作成を行う。
    """
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class UserView(RetrieveUpdateAPIView):
    """
    ユーザー詳細情報取得用のビュー。
    ユーザーの詳細情報を取得する。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

class ProfileViewSet(ModelViewSet):
    """
    プロフィール情報取得用のビュー。
    プロフィール情報を取得する。
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        """
        プロフィール情報を取得する。
        """
        if hasattr(self.request.user, 'profile'):
            sex = self.request.user.profile.sex
            # Profile.SEX[0][0] = 'male', Profile.SEX[1][0] = 'female'
            if sex == Profile.SEX[0][0]:
                reversed_sex = Profile.SEX[1][0]
            if sex == Profile.SEX[1][0]:
                reversed_sex = Profile.SEX[0][0]
            return self.queryset.filter(sex=reversed_sex)
        return self.queryset.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        プロフィール情報を作成する。
        """
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """
        プロフィール情報を削除する。
        """
        response = {'message': 'Delete is not allowed !'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """
        プロフィール情報を更新する。
        """
        response = {'message': 'Update DM is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """
        プロフィール情報を部分的に更新する。
        """
        response = {'message': 'Patch DM is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class MyProfileListView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

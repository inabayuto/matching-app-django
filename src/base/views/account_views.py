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
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

class UserView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

class ProfileViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
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
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        response = {'message': 'Delete is not allowed !'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {'message': 'Update DM is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        response = {'message': 'Patch DM is not allowed'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class MyProfileListView(RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

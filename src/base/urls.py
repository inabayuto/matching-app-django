from rest_framework.routers import DefaultRouter
from django.urls import path
from django.conf.urls import include
from base.views import ProfileViewSet, MatchingViewSet, DirectMessageViewSet, InboxListView
from base.views import CreateUserView, UserView, MyProfileListView

router = DefaultRouter()

app_name = 'base'

router.register('profiles', ProfileViewSet)
router.register('favorite', MatchingViewSet)
router.register('dm', DirectMessageViewSet, basename='dm')
router.register('dm-inbox', InboxListView, basename='dm-inbox')

urlpatterns = [
    path('users/create/', CreateUserView.as_view(), name='users-create'),
    path('users/<pk>/', UserView.as_view(), name='users'),
    path('users/profile/<uuid:pk>/', MyProfileListView.as_view(), name='users-profile'),
    path('', include(router.urls)),
]
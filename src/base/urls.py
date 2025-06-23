from rest_framework.routers import DefaultRouter
from django.urls import path
from django.conf.urls import include
from base.views import ProfileViewSet, MatchingViewSet, DirectMessageViewSet, InboxListView
from base.views import CreateUserView, UserView, MyProfileListView
from base.views.checkout_views import pay_stripe, pay_stripe_cancel, activate_user

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
    path('users/<uuid:token_id>/payment/', pay_stripe, name='pay-stripe'),  # Stripe決済画面にリダイレクト
    path('users/payment/cancel/', pay_stripe_cancel, name='pay-stripe-cancel'),  # 決済失敗時に実行
    path('users/<uuid:activate_token>/activation/', activate_user, name='users-activation'),  # 決済成功時にユーザーアクティベーションを実行
    path('', include(router.urls)),
]
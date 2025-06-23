from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import redirect
from django.conf import settings
import stripe
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from base.models import UserActivateTokens

stripe.api_key = settings.STRIPE_API_SECRET_KEY


@api_view(['GET'])
@permission_classes([AllowAny])
def pay_stripe(request, token_id):
    try:
        tokens = UserActivateTokens.objects.get(token_id=token_id)
        if tokens.is_expired():
            return Response({'message': 'トークンの有効期限が切れています'}, status=400)
        
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': settings.STRIPE_ITEM_PRICE,
                    'quantity': 1,
                },
            ],
            payment_method_types=['card'],
            mode='subscription',
            success_url=f'{settings.MY_URL}/api/users/{tokens.activate_token}/activation/',
            cancel_url=f'{settings.MY_URL}/api/users/payment/cancel/',
        )
    except UserActivateTokens.DoesNotExist:
        return Response({'message': '無効なトークンです'}, status=404)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
    return redirect(checkout_session.url, code=303)

@api_view(['GET'])
@permission_classes([AllowAny])
def pay_stripe_cancel(request):
    return Response({'message': '決済がキャンセルされました'})


@api_view(['GET'])
@permission_classes([AllowAny])
def activate_user(request, activate_token):
    activated_user = UserActivateTokens.objects.activate_user_by_token(activate_token)
    if hasattr(activated_user, 'is_active'):
        if activated_user.is_active:
            message = {'message': 'ユーザーのアクティベーションが完了しました'}
        if not activated_user.is_active:
            message = {'message': 'アクティベーションが失敗しています。管理者に問い合わせてください'}
    if not hasattr(activated_user, 'is_active'):
        message = {'message': 'エラーが発生しました'}
    return Response(message)
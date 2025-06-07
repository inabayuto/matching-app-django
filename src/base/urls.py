from rest_framework.routers import DefaultRouter
from django.urls import path
from django.conf.urls import include

router = DefaultRouter()

app_name = 'base'
urlpatterns = [
    path('', include(router.urls)),
]
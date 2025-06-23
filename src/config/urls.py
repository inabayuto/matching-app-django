from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # アプリケーションの適用
    path('api/', include('base.urls')),
    path('authen/', include('djoser.urls.jwt')),
]




   


# Takamitu/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', include('Menu.urls')),  # MenuアプリのURLをインクルード
    path('meibo/', include('Meibo.urls')),  # MeiboアプリのURLをインクルード
    path('setubi/', include('Setubi.urls')),  # SetubiアプリのURLをインクルード
    path('mitumori/', include('Mitumori.urls')),  # MitumoriアプリのURLをインクルード
]
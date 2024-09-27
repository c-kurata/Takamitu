from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', include('Menu.urls')),  # MenuアプリのURLをインクルード
    path('meibo/', include('Meibo.urls')),  # MeiboアプリのURLをインクルード
    path('mitumori/', include('Mitumori.urls')),  # MitumoriアプリのURLをインクルード
    path('reservation/', include('Setubi.urls')),  # SetubiアプリのURLを予約用にリダイレクト
    path('', lambda request: redirect('login'), name='home'),  # 最初の画面をログイン画面に設定
]
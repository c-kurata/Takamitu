from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # 管理画面のURLパターン
    path('menu/', include('Menu.urls')),  # MenuアプリのURLをインクルード
    path('meibo/', include('Meibo.urls')),  # MeiboアプリのURLをインクルード
    path('mitumori/', include('Mitumori.urls')),  # MitumoriアプリのURLをインクルード
    path('reservation/', include('Setubi.urls')),  # SetubiアプリのURLを予約用にリダイレクト
    path('', lambda request: redirect('login'), name='home'),  # 最初の画面をログイン画面に設定
]

# 開発環境でメディアファイルを提供するための設定
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('menu/', include('Menu.urls')),  # MenuアプリのURLをインクルード
    path('meibo/', include('Meibo.urls')),  # MeiboアプリのURLをインクルード
    # 'setubi/' のパスは不要になるため、削除またはコメントアウト
    # path('setubi/', include('Setubi.urls')),  
    path('mitumori/', include('Mitumori.urls')),  # MitumoriアプリのURLをインクルード
    path('reservation/', include('Setubi.urls')),  # SetubiアプリのURLを予約用にリダイレクト
    path('', lambda request: redirect('reservation_list'), name='home'),  # ルートURLにアクセス時に予約一覧にリダイレクト
]
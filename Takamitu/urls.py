from django.contrib import admin
from django.urls import path, include  # include をインポート

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Menu.urls')),  # App アプリの URL 設定
]

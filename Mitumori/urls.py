from django.urls import path
from . import views  # views モジュールをインポート

urlpatterns = [
    path('', views.index, name='mitumori_index'),  # トップページのURLパターン
    path('create/', views.create, name='mitumori_create'),  # 見積り作成ページのURLパターン
    path('list/', views.list_view, name='mitumori_list'),  # 見積りリストのURLパターン
    path('edit/<int:id>/', views.edit, name='mitumori_edit'),  # 見積り編集ページのURLパターン
]
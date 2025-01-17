from django.urls import path
from django.shortcuts import redirect  # リダイレクトのためにインポート
from . import views  # views モジュールをインポート

urlpatterns = [
    # ルートURLにアクセス時、ログインページへリダイレクト
    path('', lambda request: redirect('login'), name='home'),

    # 一般ユーザー用のログインとログアウト
    path('login/', views.login_view, name='login'),  # カスタムログインビュー
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),  # カスタムログアウトビュー

    # 新規ユーザー登録用のURL
    path('register/', views.register, name='register'),

    # メンバー関連のURL
    path('list/', views.member_list_view, name='member_list'),  # メンバー一覧表示
    path('create/', views.MemberCreateView.as_view(), name='member_create'),  # 新規メンバー作成
    path('update/<int:pk>/', views.MemberUpdateView.as_view(), name='member_update'),  # メンバー情報の更新
    path('delete/<int:pk>/', views.member_delete_view, name='member_delete'),  # メンバー削除

    # トップページ
    path('top/', views.top_view, name='top'),  # トップページ
    path('simple-list/', views.simple_member_list_view, name='simple_member_list'),  # 一般ユーザー用の簡易メンバー一覧

    # メニューからのリダイレクト用
    path('redirect/', views.meibo_redirect, name='meibo_redirect'),  # リダイレクト用のパスを追加
]
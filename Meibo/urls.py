from django.urls import path
from django.contrib.auth import views as auth_views
from Meibo import views  # 一般ユーザー登録のビューをインポート
from django.shortcuts import redirect  # 追加

urlpatterns = [
    # トップページにアクセスしたときにログインページにリダイレクト
    path('', lambda request: redirect('login')),  # '/' にアクセス時、ログインページへリダイレクト

    # 一般ユーザー用のログインとログアウト
    path('login/', views.login_view, name='login'),  # カスタムログインビュー
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),  # カスタムログアウトビュー

    # 一般ユーザー用の登録
    path('register/', views.register, name='register'),

    # メンバー関連のページのURLを短く
    path('list/', views.member_list_view, name='member_list'),  # メンバー一覧表示
    path('create/', views.MemberCreateView.as_view(), name='member_create'),  # 新規メンバー作成
    path('update/<int:pk>/', views.MemberUpdateView.as_view(), name='member_update'),  # メンバー情報の更新
    path('delete/<int:pk>/', views.member_delete_view, name='member_delete'),  # メンバー削除

    # トップページ
    path('top/', views.top_view, name='top'),  # トップページ
    path('simple-list/', views.simple_member_list_view, name='simple_member_list'),  # 一般ユーザー用の簡易メンバー一覧
]
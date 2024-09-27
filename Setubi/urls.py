from django.urls import path
from . import views  # viewsをインポート
from django.contrib.auth import views as auth_views  # 標準の認証ビューをインポート

urlpatterns = [
    path('', views.ReservationListView.as_view(), name='reservation_list'),  # 予約一覧ページ
    path('new/', views.ReservationCreateView.as_view(), name='reservation_create'),  # 新規予約作成ページ
    path('<int:pk>/edit/', views.ReservationUpdateView.as_view(), name='reservation_update'),  # 予約編集ページ
    path('<int:pk>/', views.ReservationDetailView.as_view(), name='reservation_detail'),  # 予約詳細ページ
    path('<int:pk>/delete/', views.ReservationDeleteView.as_view(), name='reservation_delete'),  # 予約削除ページ
    path('calendar/', views.CalendarView.as_view(), name='calendar'),  # カレンダー表示ページ
    path('api/reservations/', views.reservation_events, name='reservation_events'),  # 予約データ取得用API
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # ログアウト用のURLパターン
]
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, TemplateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Reservation
from .forms import ReservationForm

# 予約一覧表示ビュー
class ReservationListView(ListView):
    model = Reservation
    template_name = 'Setubi/reservation_list.html'
    context_object_name = 'reservations'

# 予約作成ビュー
class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'Setubi/reservation_form.html'
    success_url = reverse_lazy('reservation_list')

# 予約編集ビュー
class ReservationUpdateView(UpdateView):
    model = Reservation
    form_class = ReservationForm
    template_name = 'Setubi/reservation_form.html'
    success_url = reverse_lazy('reservation_list')

# 予約削除ビューを追加
class ReservationDeleteView(DeleteView):
    model = Reservation
    template_name = 'Setubi/reservation_confirm_delete.html'  # 削除確認用のテンプレート
    success_url = reverse_lazy('reservation_list')

# 予約詳細表示ビュー
class ReservationDetailView(DetailView):
    model = Reservation
    template_name = 'Setubi/reservation_detail.html'  # 詳細ページ用のテンプレート名
    context_object_name = 'reservation'

# カレンダー表示ビュー
class CalendarView(TemplateView):
    template_name = 'Setubi/calendar.html'  # カレンダーページ用のテンプレート名

# 予約データをJSON形式で返すビュー
def reservation_events(request):
    reservations = Reservation.objects.all()
    events = []

    # 設備ごとの色設定
    equipment_colors = {
        '4tユニック': '#ff9999',  # 赤色
        'ドローン（UAV）': '#99ff99',  # 緑色
        '軽トラ': '#9999ff',  # 青色
        '2tダンプ': '#5555ff',
        # 他の設備にも色を追加してください
    }

    for reservation in reservations:
        # 設備の名前に基づいて色を設定
        color = equipment_colors.get(reservation.equipment.name, '#cccccc')  # デフォルト色を設定

        events.append({
            'title': f"{reservation.equipment.name} - {reservation.facility} - {reservation.user.name}",  # イベントタイトル
            'start': reservation.start_time.strftime('%Y-%m-%dT%H:%M:%S'),  # 開始日時
            'end': reservation.end_time.strftime('%Y-%m-%dT%H:%M:%S'),      # 終了日時
            'allDay': True,  # これにより時間を表示せず、終日イベントとして扱う
            'color': color,  # 設備ごとの色を追加
        })
    return JsonResponse(events, safe=False)
from django import forms
from django.utils import timezone
from .models import Reservation
from datetime import timedelta

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['equipment', 'facility', 'start_time', 'end_time', 'user']
        labels = {
            'equipment': '車両・設備',
            'facility': '使用場所',
            'start_time': '開始日時',
            'end_time': '終了日時',
            'user': '予約者',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        now = timezone.now()
        # 現在の時間を 30 分単位に切り上げる
        start_time = (now + timedelta(minutes=30 - now.minute % 30)).replace(second=0, microsecond=0)
        end_time = (start_time + timedelta(minutes=30)).replace(second=0, microsecond=0)  # 開始から30分後の時間を設定

        self.fields['start_time'].initial = start_time  # 開始日時の初期値を設定
        self.fields['end_time'].initial = end_time  # 終了日時の初期値を設定
        
    # バリデーションで開始日時が終了日時より後でないことを確認
    def clean(self):
        cleaned_data = super().clean()
        equipment = cleaned_data.get('equipment')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # 開始日時が終了日時より後でないことを確認
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("終了日時は開始日時より後に設定してください。")

        # 予約の重複をチェック
        if equipment and start_time and end_time:
            overlapping_reservations = Reservation.objects.filter(
                equipment=equipment,
                start_time__lt=end_time,  # 自分の終了時間より前に開始されている
                end_time__gt=start_time   # 自分の開始時間より後に終了している
            ).exclude(id=self.instance.id)  # 自分自身は除外

            if overlapping_reservations.exists():
                raise forms.ValidationError(f"{equipment} はこの時間帯に既に予約されています。別の時間帯を選んでください。")
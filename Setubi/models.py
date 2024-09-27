from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string

# 色をランダムに生成する関数
def generate_random_color():
    return '#' + ''.join([get_random_string(1, 'ABCDEF0123456789') for _ in range(6)])

# 設備モデル
class Equipment(models.Model):
    name = models.CharField(max_length=100, verbose_name='設備名')  # 設備名
    description = models.TextField(blank=True, null=True, verbose_name='説明')  # 設備の説明（任意）
    serial_number = models.CharField(max_length=100, blank=True, null=True, verbose_name='シリアル番号')  # 設備のシリアル番号（任意）
    color = models.CharField(max_length=7, default=generate_random_color, verbose_name='色')  # 設備ごとの色を自動で割り当てる

    def __str__(self):
        return self.name

# 予約者モデル（従業員情報のみを持つシンプルなモデル）
class ReservationUser(models.Model):
    name = models.CharField(max_length=100, verbose_name='氏名')  # 名前のみを保持するフィールド

    def __str__(self):
        return self.name

# 予約モデル
class Reservation(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name='設備')  # 設備モデルとの関連付け
    facility = models.CharField(max_length=100, verbose_name='現場名または施設名')  # 現場名や施設名を手入力で設定
    start_time = models.DateTimeField(verbose_name='開始日時')  # 日本語のラベルを指定
    end_time = models.DateTimeField(verbose_name='終了日時')  # 日本語のラベルを指定
    user = models.ForeignKey(ReservationUser, on_delete=models.CASCADE, verbose_name='予約者')  # 予約者モデルと紐付け

    def __str__(self):
        return f"{self.equipment.name} - {self.facility} - {self.start_time} - {self.user}"

    # 予約が過去のものであるかどうかをチェックするメソッド
    def is_past_due(self):
        return self.end_time < timezone.now()

    # 予約の重複を避けるためのバリデーション
    def clean(self):
        super().clean()
        # 予約の重複をチェック
        overlapping_reservations = Reservation.objects.filter(
            equipment=self.equipment,
            start_time__lt=self.end_time,  # 自分の終了時間より前に開始されている
            end_time__gt=self.start_time   # 自分の開始時間より後に終了している
        ).exclude(id=self.id)  # 自分自身は除外

        if overlapping_reservations.exists():
            raise ValidationError(f"{self.equipment.name} はこの時間帯に既に予約されています。別の時間帯を選んでください。")
        
        # 開始時間が終了時間より後でないかチェック
        if self.start_time >= self.end_time:
            raise ValidationError("開始時間は終了時間より前である必要があります。")

    # 保存時にバリデーションを実行
    def save(self, *args, **kwargs):
        self.clean()  # バリデーションを実行
        super().save(*args, **kwargs)  # データを保存
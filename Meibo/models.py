from django.db import models

class Department(models.Model):
    id = models.AutoField(primary_key=True)  # 自動インクリメントのID
    department = models.CharField(max_length=255, unique=True)  # 部署の名前を保存する文字列フィールド
    created_at = models.DateTimeField(auto_now_add=True)  # レコード作成日時（デフォルトで現在の日時）
    updated_at = models.DateTimeField(auto_now=True)  # レコード更新日時（デフォルトで現在の日時、自動更新）

    def __str__(self):
        return self.department


class City(models.Model):
    id = models.AutoField(primary_key=True)  # 自動インクリメントのID
    city = models.CharField(max_length=255, unique=True)  # 市町村のユニークな文字列フィールド
    created_at = models.DateTimeField(auto_now_add=True)  # レコード作成日時（デフォルトで現在の日時）
    updated_at = models.DateTimeField(auto_now=True)  # レコード更新日時（デフォルトで現在の日時、自動更新）

    def __str__(self):
        return self.city


class MemberList(models.Model):
    id = models.AutoField(primary_key=True)  # 自動インクリメントのID
    user_id = models.IntegerField()  # ユーザーID
    profile_photo = models.ImageField(upload_to='photos/', blank=True, null=True)  # 顔写真
    first_name = models.CharField(max_length=255)  # 苗字
    first_name_kana = models.CharField(max_length=255)  # 苗字カナ
    last_name = models.CharField(max_length=255)  # 名前
    last_name_kana = models.CharField(max_length=255)  # 名前カナ
    city = models.ForeignKey(City, on_delete=models.CASCADE)  # 市町村（外部キー）
    address = models.CharField(max_length=255)  # 住所
    date_of_birth = models.DateField()  # 生年月日
    telephon_number = models.CharField(max_length=15, blank=True, null=True)  # 自宅電話番号
    cellular_phone_number = models.CharField(max_length=15, blank=True, null=True)  # 携帯番号
    email_address = models.EmailField(blank=True, null=True)  # メールアドレス
    department = models.ForeignKey(Department, on_delete=models.CASCADE)  # 部署（外部キー）
    date_of_entry = models.DateField()  # 入社日
    retire_age_month = models.CharField(max_length=7, blank=True, null=True)  # 定年月
    remark = models.TextField(blank=True, null=True)  # 備考
    is_admin = models.BooleanField(default=False)  # 管理者フラグ
    is_retire = models.BooleanField(default=False)  # 退職フラグ
    created_at = models.DateTimeField(auto_now_add=True)  # レコード作成日時
    updated_at = models.DateTimeField(auto_now=True)  # レコード更新日時

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
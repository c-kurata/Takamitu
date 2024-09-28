from django import forms
from .models import MemberList, City

class MemberForm(forms.ModelForm):
    class Meta:
        model = MemberList
        fields = [
            'user_id', 
            'first_name', 
            'last_name', 
            'first_name_kana', 
            'last_name_kana', 
            'city', 
            'address', 
            'date_of_birth', 
            'telephon_number', 
            'cellular_phone_number', 
            'email_address', 
            'department', 
            'date_of_entry', 
            'retire_age_month', 
            'remark', 
            'profile_photo'
        ]
        labels = {
            'user_id': 'ユーザーID',
            'first_name': '氏名（名）',
            'last_name': '氏名（姓）',
            'first_name_kana': 'フリガナ（名）',
            'last_name_kana': 'フリガナ（姓）',
            'city': '住所（市町村）',
            'address': '住所（詳細）',
            'date_of_birth': '生年月日',
            'telephon_number': '電話番号',
            'cellular_phone_number': '携帯番号',
            'email_address': 'メールアドレス',
            'department': '所属',
            'date_of_entry': '入所年月日',
            'retire_age_month': '定年月',
            'remark': '備考',
            'profile_photo': '顔写真',
        }
        widgets = {
            'user_id': forms.TextInput(attrs={'placeholder': 'ユーザーIDを入力', 'style': 'width: 200px;'}),
            'first_name': forms.TextInput(attrs={'placeholder': '名', 'style': 'width: 200px;'}),
            'last_name': forms.TextInput(attrs={'placeholder': '姓', 'style': 'width: 200px;'}),
            'first_name_kana': forms.TextInput(attrs={'placeholder': '氏名カナ（名）', 'style': 'width: 200px;'}),
            'last_name_kana': forms.TextInput(attrs={'placeholder': '氏名カナ（姓）', 'style': 'width: 200px;'}),
            'address': forms.TextInput(attrs={'placeholder': '住所詳細', 'style': 'width: 400px;'}),  # 住所詳細の幅を調整
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'style': 'width: 200px;'}),
            'telephon_number': forms.TextInput(attrs={'placeholder': 'ハイフン無しの0から9半角数字', 'style': 'width: 200px;'}),
            'cellular_phone_number': forms.TextInput(attrs={'placeholder': 'ハイフン無しの0から9半角数字', 'style': 'width: 200px;'}),
            'email_address': forms.EmailInput(attrs={'placeholder': 'メールアドレス', 'style': 'width: 300px;'}),
            'department': forms.Select(attrs={'style': 'width: 200px;'}),  # 部署の選択フィールドも調整
            'date_of_entry': forms.DateInput(attrs={'type': 'date', 'style': 'width: 200px;'}),
            'retire_age_month': forms.TextInput(attrs={'placeholder': 'yyyy/MM', 'style': 'width: 200px;'}),
            'remark': forms.Textarea(attrs={'placeholder': '備考', 'rows': 3, 'style': 'width: 400px;'}),  # 備考も調整
            'profile_photo': forms.ClearableFileInput(attrs={'style': 'width: 200px;'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 市町村を選択肢として表示
        self.fields['city'].queryset = City.objects.all()
        self.fields['city'].widget.attrs.update({'style': 'width: 200px;'})

    def clean(self):
        cleaned_data = super().clean()
        date_of_birth = cleaned_data.get('date_of_birth')
        
        # 生年月日から定年月を自動計算
        if date_of_birth:
            retirement_age = 65
            retirement_year = date_of_birth.year + retirement_age
            retirement_month = date_of_birth.month
            cleaned_data['retire_age_month'] = f"{retirement_year}/{retirement_month:02d}"
        
        return cleaned_data
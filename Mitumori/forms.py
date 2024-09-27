from django import forms
from django.core.exceptions import ValidationError
from .models import Estimate, Department, Employee

# PDFファイルを検証する関数
def validate_pdf(file):
    if file and not file.name.endswith('.pdf'):
        raise ValidationError("PDFファイルをアップロードしてください。")

# 見積もりフォーム
class EstimateForm(forms.ModelForm):
    class Meta:
        model = Estimate
        fields = [
            'estimate_name',
            'submit_to_name',
            'estimate_amount',
            'summary',
            'created_by',
            'last_updated_by',
            'admin_approval_status',
            'department',
            'submission_date',
            'attachment'
        ]
        labels = {
            'estimate_name': '見積名',
            'submit_to_name': '提出先名',
            'estimate_amount': '見積金額',
            'summary': '概要',
            'created_by': '作成者ID',
            'last_updated_by': '最終更新者ID',
            'admin_approval_status': '管理者承認状態',
            'department': '部署ID',
            'submission_date': '提出日',
            'attachment': '添付ファイル'
        }
        widgets = {
            'submission_date': forms.DateInput(attrs={'type': 'date'}),
        }

    # コンストラクタで除外フィールドを設定
    def __init__(self, *args, **kwargs):
        exclude_fields = kwargs.pop('exclude_fields', None)
        super(EstimateForm, self).__init__(*args, **kwargs)
        if exclude_fields:
            for field in exclude_fields:
                self.fields.pop(field)

    # 添付ファイルの検証ロジック
    def clean_attachment(self):
        attachment = self.cleaned_data.get('attachment')
        validate_pdf(attachment)
        return attachment

# 見積もり検索フォーム
class EstimateSearchForm(forms.Form):
    estimate_id = forms.IntegerField(label='見積ID', required=False)
    keyword = forms.CharField(label='キーワード', max_length=255, required=False)
    submit_to_name = forms.ChoiceField(
        label='提出先',
        choices=[('', '選択してください')] + [(s, s) for s in Estimate.objects.values_list('submit_to_name', flat=True).distinct()],
        required=False
    )
    department = forms.ModelChoiceField(label='部署名', queryset=Department.objects.all(), required=False)
    created_by = forms.ModelChoiceField(label='作成者', queryset=Employee.objects.all(), required=False)
    submission_date_from = forms.DateField(
        label='提出日 (開始)', required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
    submission_date_to = forms.DateField(
        label='提出日 (終了)', required=False, widget=forms.DateInput(attrs={'type': 'date'})
    )
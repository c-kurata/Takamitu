import pdfplumber
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from .forms import EstimateForm, EstimateSearchForm
from .models import Estimate
from django.db.models import Q  # フィルタリングで使用

# PDFファイルからテキストを抽出する関数
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# トップページの表示
def index(request):
    return render(request, 'Mitumori/index.html')

# 見積もり作成ページの処理
def create(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')
        if pdf_file:
            text = extract_text_from_pdf(pdf_file)
            data = {
                'estimate_name': '見積名',
                'submit_to_name': '提出先名',
                'estimate_amount': 12345.67,
                'summary': text,
                'created_by': 1,  # ここに正しい作成者IDを設定します
                'department': 1,  # ここに正しい部署IDを設定します
                'submission_date': '2024-07-01',
            }
            form = EstimateForm(data, exclude_fields=['last_updated_by', 'admin_approval_status'])
        else:
            form = EstimateForm(request.POST, request.FILES, exclude_fields=['last_updated_by', 'admin_approval_status'])
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.last_updated_by = instance.created_by  # 最終更新者を作成者と同じに設定
            instance.admin_approval_status = '未承認'  # 初期状態で未承認とする
            instance.save()
            return redirect('mitumori:list')  # URL名前空間を使用してリダイレクト
        else:
            print(form.errors)  # エラーメッセージをコンソールに表示
    else:
        form = EstimateForm(exclude_fields=['last_updated_by', 'admin_approval_status'])
    return render(request, 'Mitumori/create.html', {'form': form})

# 見積もりリスト表示と検索
def list(request):
    form = EstimateSearchForm(request.GET or None)
    estimates = Estimate.objects.all()

    if form.is_valid():
        if form.cleaned_data['estimate_id']:
            estimates = estimates.filter(id=form.cleaned_data['estimate_id'])
        if form.cleaned_data['keyword']:
            estimates = estimates.filter(estimate_name__icontains=form.cleaned_data['keyword'])
        if form.cleaned_data['submit_to_name']:
            estimates = estimates.filter(submit_to_name=form.cleaned_data['submit_to_name'])
        if form.cleaned_data['department']:
            estimates = estimates.filter(department=form.cleaned_data['department'])
        if form.cleaned_data['created_by']:
            estimates = estimates.filter(created_by=form.cleaned_data['created_by'])
        if form.cleaned_data['submission_date_from']:
            estimates = estimates.filter(submission_date__gte=form.cleaned_data['submission_date_from'])
        if form.cleaned_data['submission_date_to']:
            estimates = estimates.filter(submission_date__lte=form.cleaned_data['submission_date_to'])

    return render(request, 'Mitumori/list.html', {'form': form, 'estimates': estimates})

# 見積もり編集ページの処理
def edit(request, id):
    estimate = get_object_or_404(Estimate, id=id)
    if request.method == 'POST':
        form = EstimateForm(request.POST, request.FILES, instance=estimate)
        if form.is_valid():
            form.save()
            return redirect('mitumori:list')
    else:
        form = EstimateForm(instance=estimate)
    return render(request, 'Mitumori/edit.html', {'form': form})
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
            text += page.extract_text() or ""  # テキストを抽出し、Noneの場合は空文字に置き換える
    return text

# トップページの表示
def index(request):
    return render(request, 'Mitumori/index.html')

# 見積もり作成ページの処理
def create(request):
    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')  # PDFファイルを取得
        if pdf_file:
            text = extract_text_from_pdf(pdf_file)  # PDFからテキストを抽出
            data = {
                'estimate_name': '見積名',  # デフォルトの見積名を設定（必要に応じて修正）
                'submit_to_name': '提出先名',  # デフォルトの提出先名を設定（必要に応じて修正）
                'estimate_amount': 12345.67,  # デフォルトの金額を設定（必要に応じて修正）
                'summary': text,  # 抽出したテキストを要約に設定
                'created_by': request.user.id,  # 作成者をログイン中のユーザーに設定
                'department': 1,  # ここに正しい部署IDを設定（適切に変更してください）
                'submission_date': '2024-07-01',  # 提出日を設定（適宜変更してください）
            }
            form = EstimateForm(data, exclude_fields=['last_updated_by', 'admin_approval_status'])
        else:
            form = EstimateForm(request.POST, request.FILES, exclude_fields=['last_updated_by', 'admin_approval_status'])
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.last_updated_by = request.user  # 最終更新者をログイン中のユーザーに設定
            instance.admin_approval_status = '未承認'  # 初期状態で未承認に設定
            instance.save()
            return redirect('mitumori_list')  # 見積もりリストページにリダイレクト
        else:
            print(form.errors)  # エラーメッセージをコンソールに表示
    else:
        form = EstimateForm(exclude_fields=['last_updated_by', 'admin_approval_status'])
    return render(request, 'Mitumori/create.html', {'form': form})

# 見積もりリスト表示と検索
def list_view(request):
    form = EstimateSearchForm(request.GET or None)  # 検索フォームを取得
    estimates = Estimate.objects.all()  # すべての見積もりを取得

    if form.is_valid():  # フォームが有効な場合のみフィルタリングを行う
        if form.cleaned_data['estimate_id']:
            estimates = estimates.filter(id=form.cleaned_data['estimate_id'])
        if form.cleaned_data['keyword']:
            estimates = estimates.filter(estimate_name__icontains=form.cleaned_data['keyword'])
        if form.cleaned_data['submit_to_name']:
            estimates = estimates.filter(submit_to_name__icontains=form.cleaned_data['submit_to_name'])
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
    estimate = get_object_or_404(Estimate, id=id)  # 見積もりを取得、なければ404エラー
    if request.method == 'POST':
        form = EstimateForm(request.POST, request.FILES, instance=estimate)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.last_updated_by = request.user  # 最終更新者をログイン中のユーザーに設定
            instance.save()
            return redirect('mitumori_list')  # 編集後、見積もりリストページにリダイレクト
    else:
        form = EstimateForm(instance=estimate)
    return render(request, 'Mitumori/edit.html', {'form': form})
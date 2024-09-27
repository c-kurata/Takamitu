from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import MemberList
from .forms import MemberForm
from django.views import View
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView

# 社員の新規作成ビュー (クラスベース)
class MemberCreateView(LoginRequiredMixin, View):  # ログイン必須
    def get(self, request):
        form = MemberForm()
        return render(request, 'Meibo/create.html', {'form': form})

    def post(self, request):
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "社員が正常に登録されました。")
            return redirect(reverse('member_list'))
        messages.error(request, "入力にエラーがあります。もう一度確認してください。")
        return render(request, 'Meibo/create.html', {'form': form})

# メンバーの一覧表示ビュー (関数ベース)
@login_required  # ログイン必須
def member_list_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        members = MemberList.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(first_name_kana__icontains=search_query) |
            Q(last_name_kana__icontains=search_query) |
            Q(city__city__icontains=search_query) |
            Q(department__department__icontains=search_query)
        )
    else:
        members = MemberList.objects.all()

    return render(request, 'Meibo/list.html', {'members': members, 'search_query': search_query})

# 簡易メンバーリストビュー (一般ユーザー用)
@login_required  # ログイン必須
def simple_member_list_view(request):
    search_query = request.GET.get('search', '')
    if search_query:
        members = MemberList.objects.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(department__department__icontains=search_query)
        )
    else:
        members = MemberList.objects.all()

    return render(request, 'Meibo/simple_list.html', {'members': members, 'search_query': search_query})

# トップページの表示ビュー
@login_required  # ログイン必須
def top_view(request):
    return render(request, 'Meibo/top.html')

# メンバー情報の更新ビュー (クラスベース)
class MemberUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        member = get_object_or_404(MemberList, pk=pk)
        form = MemberForm(instance=member)
        return render(request, 'Meibo/update.html', {'form': form, 'member': member})

    def post(self, request, pk):
        member = get_object_or_404(MemberList, pk=pk)
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            # 更新後も同じページに留まり、メッセージを表示する
            messages.success(request, "社員情報が正常に更新されました。")
            # リダイレクトではなく、同じテンプレートを再度レンダリングして表示
            return render(request, 'Meibo/update.html', {'form': form, 'member': member, 'success': True})

        messages.error(request, "入力にエラーがあります。もう一度確認してください。")
        return render(request, 'Meibo/update.html', {'form': form, 'member': member, 'success': False})

# メンバー情報の削除ビュー
@login_required
def member_delete_view(request, pk):
    member = get_object_or_404(MemberList, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, "社員情報が正常に削除されました。")
        return redirect('member_list')
    return render(request, 'Meibo/delete_confirm.html', {'member': member})

# 新規ユーザー登録ビュー
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # ユーザーを登録後、自動的にログインさせる
            messages.success(request, "アカウントが正常に作成されました。")
            return redirect('top')  # トップページにリダイレクト
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# ログインビュー
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"ようこそ、{username} さん！")
                
                # 管理者と一般ユーザーでリダイレクト先を変更
                if user.is_superuser or user.is_staff:
                    return redirect('top')  # 管理者用のトップページ
                else:
                    return redirect('simple_member_list')  # 一般ユーザー用のトップページ
        else:
            messages.error(request, "ユーザー名かパスワードが正しくありません。")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# ログアウトビュー (Django標準のLogoutViewを使用)
class CustomLogoutView(LogoutView):
    template_name = 'registration/logged_out.html'
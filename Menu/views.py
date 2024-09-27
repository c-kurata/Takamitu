from django.shortcuts import render
from django.contrib.auth.decorators import login_required  # ログイン必須デコレーターをインポート

@login_required  # ログイン必須
def menu_view(request):
    user = request.user  # ログイン中のユーザー情報を取得
    context = {
        'is_admin': user.is_staff or user.is_superuser  # 管理者かどうかをチェックしてコンテキストに渡す
    }
    return render(request, 'Menu/menu.html', context)  # メニュー画面を表示し、コンテキストを渡す
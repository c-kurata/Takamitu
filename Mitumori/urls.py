from django.urls import path
from . import views  # この行を確認または追加

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('list/', views.list, name='list'),
    path('edit/<int:id>/', views.edit, name='edit'),
]

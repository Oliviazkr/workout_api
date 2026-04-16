from django.urls import path
from . import views

urlpatterns = [
    # 首页
    path('', views.home, name='home'),

    # 认证
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 食物管理
    path('foods/', views.food_list, name='food_list'),
    path('foods/add/', views.food_add, name='food_add'),
    path('foods/<int:pk>/edit/', views.food_edit, name='food_edit'),
    path('foods/<int:pk>/delete/', views.food_delete, name='food_delete'),
    path('foods/import/', views.import_csv, name='import_csv'),

    # 计算
    path('calculate/', views.calculate_nutrition, name='calculate'),

    # 历史
    path('history/', views.history_list, name='history'),
    path('history/<int:pk>/', views.history_detail, name='history_detail'),

    # API
    path('api/search/', views.search_foods, name='search_foods'),
]

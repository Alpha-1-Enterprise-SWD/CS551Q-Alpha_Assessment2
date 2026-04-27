from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('practice/<str:practice_code>/', views.practice_detail, name='practice_detail'),
    path('api/analytics/', views.analytics_api, name='analytics_api'),
]

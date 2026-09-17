from django.urls import path
from .views import index_view, DashboardStatsAPIView

app_name = 'dashboard'

urlpatterns = [
    path('', index_view, name='index'),
    path('api/stats/', DashboardStatsAPIView.as_view(), name='api_stats'),
]

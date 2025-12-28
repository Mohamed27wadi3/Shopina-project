from django.urls import path

from .views import DashboardStatsView, OrderDetailView, OrderListCreateView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='orders'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]

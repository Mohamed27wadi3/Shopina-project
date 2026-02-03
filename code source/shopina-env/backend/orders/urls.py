from django.urls import path

from .views import DashboardStatsView, OrderDetailView, OrderListCreateView, OrdersImportPageView

urlpatterns = [
    path('', OrderListCreateView.as_view(), name='orders'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('import/', OrdersImportPageView.as_view(), name='orders-import'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]

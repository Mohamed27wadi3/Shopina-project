from django.urls import path
from .views import (
    MyShopRedirectView,
    CreateShopView,
    ShopDashboardView,
    UpdateShopView,
    get_my_shop,
    create_shop_api,
    save_theme,
)

app_name = 'shop'

urlpatterns = [
    # HTML views
    path('my-shop/', MyShopRedirectView.as_view(), name='my-shop'),
    path('create/', CreateShopView.as_view(), name='create'),
    path('<slug:slug>/dashboard/', ShopDashboardView.as_view(), name='dashboard'),
    path('settings/', UpdateShopView.as_view(), name='settings'),
    
    # API endpoints
    path('api/my-shop/', get_my_shop, name='api-my-shop'),
    path('api/create/', create_shop_api, name='api-create'),
    path('api/theme/', save_theme, name='api-theme'),
]

from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    CategoryViewSet,
    ProductViewSet,
    create_product_api,
    public_shop_products,
    update_product_api,
    delete_product_api,
    announcements_list,
    public_shop_announcements,
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('create/', create_product_api, name='api-create-product'),
    path('public/<slug:slug>/products/', public_shop_products, name='api-public-products'),
    path('<int:product_id>/update/', update_product_api, name='api-update-product'),
    path('<int:product_id>/delete/', delete_product_api, name='api-delete-product'),
    path('announcements/', announcements_list, name='api-announcements'),
    path('public/<slug:slug>/announcements/', public_shop_announcements, name='api-public-announcements'),
]

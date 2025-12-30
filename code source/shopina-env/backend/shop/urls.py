from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, create_product_api, public_shop_products
from .views import update_product_api, delete_product_api

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('api/create/', create_product_api, name='api-create-product'),
    path('api/public/<slug:slug>/products/', public_shop_products, name='api-public-products'),
    path('api/<int:product_id>/update/', update_product_api, name='api-update-product'),
    path('api/<int:product_id>/delete/', delete_product_api, name='api-delete-product'),
]

"""
URL configuration for shopina project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.views.generic.base import RedirectView

from .views import DashboardView, CreateOrderView, CreateProductView, ProfileDynamicView
from .views import ClientsListPageView, FrontendIndexView
from shops.views import MyShopRedirectView
from orders.views import OrdersListPageView, OrderDetailPageView

urlpatterns = [
    path('api/templates/', include('templates.urls')),
    path('admin/', admin.site.urls),
    # Redirect to frontend (React app on port 3000 in dev, or built files in production)
    path('', FrontendIndexView.as_view(), name='home'),
    path('public/', TemplateView.as_view(template_name='public_home.html'), name='public-home'),
    # Authentication (non-admin)
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),  # allauth social auth

    # Static profile demo page (animated) - requires authentication
    path('profile-dynamic/', ProfileDynamicView.as_view(), name='profile_dynamic'),

    # Dashboard (HTML template)
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile-settings/', TemplateView.as_view(template_name='profile_settings.html'), name='profile-settings'),
    path('orders/', OrdersListPageView.as_view(), name='orders-page'),
    path('orders/<int:pk>/', OrderDetailPageView.as_view(), name='order-detail'),
    path('orders/create/', CreateOrderView.as_view(), name='create-order'),
    path('products/create/', CreateProductView.as_view(), name='create-product'),
    path('clients/', ClientsListPageView.as_view(), name='clients-page'),
    # Root-level My Shop redirect
    path('my-shop/', MyShopRedirectView.as_view(), name='my-shop'),
    
    # Shop URLs (HTML views and API)
    path('shop/', include('shops.urls')),
    path('templates/', TemplateView.as_view(template_name='templates_marketplace.html'), name='templates-marketplace'),
    path('checkout/', TemplateView.as_view(template_name='checkout.html'), name='checkout'),

    # Legal & Trust pages
    path('legal/about/', TemplateView.as_view(template_name='legal/about.html'), name='about'),
    path('legal/contact/', TemplateView.as_view(template_name='legal/contact.html'), name='contact'),
    path('legal/terms/', TemplateView.as_view(template_name='legal/terms.html'), name='terms'),
    path('legal/privacy/', TemplateView.as_view(template_name='legal/privacy.html'), name='privacy'),
    path('legal/cookies/', TemplateView.as_view(template_name='legal/cookies.html'), name='cookies'),
    path('legal/rights/', TemplateView.as_view(template_name='legal/rights.html'), name='rights'),
    
    # API endpoints
    path('api/users/', include('users.urls')),
    path('api/shop/', include('shop.urls')),
    path('api/carts/', include('carts.urls')),
    path('api/orders/', include('orders.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/notifications/', include('notifications.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

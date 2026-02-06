from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, 
    ProfileView, 
    CustomTokenObtainPairView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ChangePasswordView,
    TwoFactorStartView,
    TwoFactorVerifyView,
    UserListView,
    UserDetailView,
    UserStatisticsView,
    CustomerListView,
    CustomerDetailView,
)
from .session_views import (
    LoginWithSessionView,
    LogoutWithSessionView,
    ExtendSessionView,
    GetSessionInfoView,
)
from .html_views import ProfileHTMLView, ChangePasswordHTMLView
from .social_views import google_login, github_login, remember_me_login

app_name = 'users'

urlpatterns = [
    # ✅ ENHANCED Authentication with Session Management
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # ✅ NEW: Session-based authentication (prevents logout on navigation)
    path('auth/login-with-session/', LoginWithSessionView.as_view(), name='login_with_session'),
    path('auth/logout-with-session/', LogoutWithSessionView.as_view(), name='logout_with_session'),
    path('auth/extend-session/', ExtendSessionView.as_view(), name='extend_session'),
    path('auth/session-info/', GetSessionInfoView.as_view(), name='session_info'),
    
    # Social Login
    path('auth/google/', google_login, name='google_login'),
    path('auth/github/', github_login, name='github_login'),
    path('auth/remember-me/', remember_me_login, name='remember_me_login'),
    
    # Profile (API)
    path('profile/', ProfileView.as_view(), name='profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    
    # Profile (HTML) - For Django session authentication
    path('profile-page/', ProfileHTMLView.as_view(), name='profile_html'),
    path('change-password-page/', ChangePasswordHTMLView.as_view(), name='change_password_html'),
    
    # Password Reset
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Two-factor
    path('2fa/start/', TwoFactorStartView.as_view(), name='2fa_start'),
    path('2fa/verify/', TwoFactorVerifyView.as_view(), name='2fa_verify'),
    
    # User Management (Admin)
    path('', UserListView.as_view(), name='user_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('statistics/', UserStatisticsView.as_view(), name='user_statistics'),
    path('customers/', CustomerListView.as_view(), name='customer_list'),
    path('customers/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
]

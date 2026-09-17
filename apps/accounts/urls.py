from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomTokenObtainPairView,
    UserProfileAPIView,
    ChangePasswordAPIView,
    UserViewSet,
    login_view,
    logout_view,
    profile_view
)

app_name = 'accounts'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Web Auth Routes
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),

    # API Auth Routes
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='api_login'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('api/auth/profile/', UserProfileAPIView.as_view(), name='api_profile'),
    path('api/auth/change-password/', ChangePasswordAPIView.as_view(), name='api_change_password'),
    path('api/', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'kyc', KYCViewSet)
router.register(r'wallet', WalletViewSet)


schema_view = get_schema_view(
    openapi.Info(
        title="Crystal API",
        default_version='v1',
        description="API documentation for E-money Banking System",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@e-money.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('', include(router.urls)),
    path("api/auth/register/", RegisterView.as_view(), name="auth_register"),
    path("api/auth/login/", LoginView.as_view(), name="auth_login"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . views import *
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'cards', CardViewSet)

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
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
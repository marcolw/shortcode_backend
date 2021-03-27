from django.urls import path, include
from rest_framework import routers

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import apis


router = routers.DefaultRouter()
router.register('users', apis.UserViewSet, basename="users")

urlpatterns = [
    path('obtain-token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += router.urls

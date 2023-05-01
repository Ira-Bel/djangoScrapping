from django.urls import path
from . import views

from .views import RegisterAPIView, ActivateAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path("users/", views.ShowUsersAPIViews.as_view()),
    path("items/", views.ShowAllGoodsAPIView.as_view()),

    path("register/", RegisterAPIView.as_view()),
    path("activate/<uid>/<token>/", ActivateAPIView.as_view()),
    path("plot/<str:name>/", views.GoodsPriceAPIView.as_view()),
]

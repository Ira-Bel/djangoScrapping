from django.urls import path
from . import views

from .views import RegisterAPIView, ActivateAPIView, UserLoginAPIView

urlpatterns = [

    path("users/", views.ShowUsersAPIViews.as_view()),
    path("items/", views.ShowAllGoodsAPIView.as_view()),

    path("register/", RegisterAPIView.as_view()),
    path("activate/<uid>/<token>/", ActivateAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
    path("plot/<str:name>/", views.GoodsPriceAPIView.as_view()),
]

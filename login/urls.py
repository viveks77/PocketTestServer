from django.urls import path
from .api import LoginAPI, RegisterAPI, UserAPI, ResetPasswordAPI, UserUpdateAPI, ClassListAPI
from knox.views import LogoutView

urlpatterns = [
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPI.as_view()),
    path('userinfo', UserAPI.as_view()),
    path('logout',LogoutView.as_view()),
    path('resetpass',ResetPasswordAPI.as_view()),
    path('update',UserUpdateAPI.as_view()),
    path('getclass',ClassListAPI.as_view()),
]
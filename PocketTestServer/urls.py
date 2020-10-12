"""PocketTestServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import login
import quiz
from quiz.Views.Views import views
#from django.contrib.auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('login.urls')),
    path('signup', views.StaffSignupView.as_view(), name='signup'),
    path('login',views.staffLoginView, name='login'),
    path('',include('quiz.urls')),
    path('',views.staffLoginView),
]

handler404 = 'login.views.handler404'
handler500 = 'login.views.handler500'
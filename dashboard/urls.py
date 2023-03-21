from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('login' , login_view , name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    
]

from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('add_templates/', add_template_view, name="add_template_view"),
    path('manage_templates/', manage_templates, name="manage_templates"),
    path('update_view/<int:id>/' , update_view , name="update_view"),
    path('delete_view/<int:id>/' , delete_view , name="delete_view"),
    path('login' , login_view , name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

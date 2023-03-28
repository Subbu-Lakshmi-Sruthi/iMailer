from django.urls import path, include
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('add_templates/', add_template_view, name="add_template_view"),
    path('manage_templates/', manage_templates, name="manage_templates"),
    path('update_template/<int:id>/' , update_template , name="update_template"),
    path('delete_template/<int:id>/' , delete_template , name="delete_template"),
    path('login' , login_view , name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('send_mail/',send_mail,name="send_mail"),
    path('send_mail_bulk/',send_mail_bulk,name="send_mail_bulk"),
    path('get_image/<int:id>/',read_recipient,name="update-read-status")
]

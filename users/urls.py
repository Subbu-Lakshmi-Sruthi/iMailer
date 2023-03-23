from django.urls import path
from .views import *

urlpatterns = [
    path('',profile,name="profile"),
    path('add-group', add_group , name="add_group"),
    path('manage-access' , manage_access , name="manage_access" ),
]
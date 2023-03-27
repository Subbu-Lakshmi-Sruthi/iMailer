from django.urls import path
from .views import *

urlpatterns = [
    path('',profile,name="profile"),
    path('add-group', add_group , name="add_group"),
    path('manage-access' , manage_access , name="manage_access" ),
    path('manage-user-permission' , manage_user_permission , name="manage_user_permission" ),
    path('manage-permission' , manage_permission , name="manage_permission" ),
    path('manage-permission-update/<int:id>' , manage_pre_update , name='manage_pre_update'),
    path('manage-permission-delete/<int:id>' , manage_pre_delete , name='manage_pre_delete'),
]
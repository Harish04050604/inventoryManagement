from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'), # 1st page
    path('signup/',views.signup,name='signup'),
    path('login/', views.login, name='login'),
    path('manager/', views.manager, name='manager'),
    path('staff/', views.staff, name='staff'),
    path('view_tasks/', views.view_tasks, name='view_tasks'),
    path('add_items/', views.add_items, name='add_items'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('delete-item/', views.delete_item, name='delete_item'),
    path('task-list/', views.task_list, name='task_list'),
    path('edit/<str:item_name>/', views.edit_item, name='edit_item'),]
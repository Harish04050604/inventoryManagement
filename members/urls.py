from django.urls import path
from . import views
from .views import generate_report, generate_pdf

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
    path('edit/<str:item_name>/', views.edit_item, name='edit_item'),
    path('sell/<str:item_name>/', views.sell_item, name='sell_item'),
    path('view_report/', generate_report, name='view_report'),
    path('generate_pdf/', generate_pdf, name='generate_pdf'),
    path('add/<str:item_name>/', views.add_item, name='add_item'), 
    path('delete-item/<str:item_name>/', views.delete_item, name='delete_item'),
]
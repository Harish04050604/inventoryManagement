from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'), # 1st page
    path('signup/',views.signup,name='signup'),
    path('login/', views.login, name='login'),
    path('manager/', views.manager, name='manager'),
    path('staff/', views.staff, name='staff'),
    path('view-tasks/', views.view_tasks, name='view_tasks'),
    path('add-items/', views.add_items, name='add_items'),
    path('update-quantity/', views.update_quantity, name='update_quantity'),
]
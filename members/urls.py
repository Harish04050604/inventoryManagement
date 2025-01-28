from django.urls import path
from . import views

urlpatterns = [
    path('',views.login,name='login'), # 1st page
    path('signup/',views.signup,name='signup'),
    path('login/', views.login, name='login'),
    path('manager/', views.manager, name='manager'),
    path('staff/', views.staff, name='staff'),
]
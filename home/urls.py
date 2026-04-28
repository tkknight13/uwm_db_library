from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('signup/', views.signup_view, name='signup'),
    path('student_home/', views.student_home, name='student_home'),
    path('books/', views.view_books, name='view_books'),
]
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
    path('admin-home/', views.admin_home, name='admin_home'),
    path('admin-home/add/', views.add_book, name='add_book'),
    path('admin-home/edit/<int:pk>/', views.edit_book, name='edit_book'),
    path('admin-home/delete/<int:pk>/', views.delete_book, name='delete_book'),
    path('checkout/<int:pk>/', views.checkout_book, name='checkout_book'),
    path('users/', views.view_users, name='view_users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
]
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [

    path('register/',views.registerPage,name='register'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),

    path('', views.home,name='home'), 
    path('user/',views.userPage,name='user-page'),  
    path('customer/<str:pk>/', views.customer,name='customer'),

    path('add_book/<str:pk>/', views.addBook,name='add_book'),
    path('update_book/<str:pk>/', views.updateBook,name='update_book'),
    path('delete_book/<str:pk>/', views.deleteBook,name='delete_book'),
    
    path('add_customer/', views.addCustomer,name='add_customer'),
    path('update_customer/<str:pk>/', views.updateCustomer,name='update_customer'),
    path('delete_customer/<str:pk>/', views.deleteCustomer,name='delete_customer'),

    path('add_book_user/<str:pk>',views.addBookUser,name='add_book_user'),
    path('update_book_user/<str:pk>',views.updateBookUser,name='update_book_user'),
    path('delete_book_user/<str:pk>',views.deleteBookUser,name='delete_book_user'),

    path('make_admin/<str:pk>',views.makeAdmin,name='make_admin'),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name='BooksApp/password_reset.html'),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name='BooksApp/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='BooksApp/password_reset_form.html'),name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='BooksApp/password_reset_done.html'),name='password_reset_complete'),
]

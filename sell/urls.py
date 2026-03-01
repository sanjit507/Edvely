from django.urls import path
from . import views 
from django.contrib.auth import views as auth_views

urlpatterns=[ path('', views.home, name='home'),
             path('course/<str:slug>/', views.course_detail, name='course_detail'),
             path('login/', auth_views.LoginView.as_view(), name='login'),
             path('logout/', auth_views.LogoutView.as_view(), name='logout'),
             path('dashboard/',views.dashboard,name="dashboard"),
             path('register/',views.register,name='register'),
             path('profile/', views.profile_view, name='profile'),
             path('checkout/<slug:slug>/',views.checkout,name='checkout'),
             path('payment_success',views.payment_success,name='payment_success')

             
             
             
             
    ]
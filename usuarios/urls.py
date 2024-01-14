from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_View, name='login'),
    path('logout', views.logout_django, name='logout'),
]
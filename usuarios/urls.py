from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_View, name='login'),
    path('logout', views.logout_django, name='logout'),

    path('cadastrar-usuarios', views.cadastrar_usuários, name='cadastrar-usuarios'),
    path('lista-de-usuarios', views.lista_de_usuarios, name='lista-de-usuarios'),
    path('editar-usuarios/<int:pk>', views.atualizar_usuario, name='editar-usuarios'),
]
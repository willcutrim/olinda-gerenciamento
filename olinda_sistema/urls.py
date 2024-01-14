
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('produtos.urls')),
    path('', include('caixa.urls')),
    path('', include('relatorios.urls')),
    path('', include('usuarios.urls')),

]

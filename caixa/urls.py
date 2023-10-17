from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('post-caixa', views.PostFrenteCaixa.as_view()),
    path('historico-vendas', views.historico_de_vendas, name="historico-vendas"),
    path('caixa', views.caixa, name="caixa"),
]
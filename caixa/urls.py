from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('post-caixa', views.PostFrenteCaixa.as_view()),
    path('historico-vendas', views.historico_de_vendas, name="historico-vendas"),
    path('deletar_venda/<int:id>', views.deletar_venda, name="deletar-venda"),
    path('caixa', views.caixa, name="caixa"),

    path('get-price/', views.get_product_price, name='get_product_price'),
]
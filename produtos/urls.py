from django.urls import path
from . import views

urlpatterns = [ 
    path('get-produtos', views.GetAllProducts.as_view()),
    path('produtos', views.produtos, name="produtos"),
    path('cadastro-produto', views.cadastro_de_produtos, name='cadastro-produto'),
    path('deletar_produto/<int:id>', views.deletar_produto, name='deletar-produto'),

    path('create-category/', views.create_category, name='create_category'),
]
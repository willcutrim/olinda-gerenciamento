from django.urls import path
from . import views

urlpatterns = [
    path('relatorio', views.relatorio, name='relatorio'),
    path('add-relatorio', views.add_despesas, name='add_relatorio'),
    path('data-relatorio', views.DataRelatorio.as_view()),
    path('data-all-relatorio', views.DataAllRelatorio.as_view()),
]
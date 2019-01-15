from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('controle/', views.controle, name='controle'),
    path('movimentos/', views.movimentos, name='movimentos'),
    path('edit-prod/<int:pk>/', views.edit_prod, name='edit_prod'),
    path('sobre/', views.sobre, name='sobre')
]

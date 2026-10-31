# Rutas del listado y de las operaciones CRUD.

from django.urls import path
from . import views

app_name = 'clients'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]

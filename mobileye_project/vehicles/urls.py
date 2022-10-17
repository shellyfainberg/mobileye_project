from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.list, name='list'),
    path('<int:vehicle_id>/occupy/', views.occupy, name='occupy'),
    path('<int:vehicle_id>/release/', views.release, name='release'),
    path('<str:license_plate_number>/history/', views.history, name='history'),
]


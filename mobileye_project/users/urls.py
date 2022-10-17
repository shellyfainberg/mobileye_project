from django.urls import path

from . import views

urlpatterns = [
    path('detail/<int:pk>/', views.UserDetail.as_view(), name="user-detail"),
    path('detail/<int:pk>/', views.UserList.as_view(), name="user-list"),
]
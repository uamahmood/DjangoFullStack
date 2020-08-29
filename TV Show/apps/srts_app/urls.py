from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('shows', views.AllShows),
    path('shows/new', views.AddNewShow),
    path('shows/create', views.CreateNewShow),
    path('shows/<int:id>/', views.TvShow),
    path('shows/<int:id>/edit', views.EditShow),
    path('shows/<int:id>/update', views.UpdateShow),
    path('shows/<int:id>/destroy', views.DeleteShow)
]
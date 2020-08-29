from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('wall', views.wall),
    path('logout', views.logout),
    path('login', views.login),
    path('messages/create', views.messages_create),
    path('comments/create', views.comments_create),
    path('messages/<int:message_id>/delete', views.messages_delete),
    path('messages/<int:message_id>/like', views.messages_like),
    path('messages/<int:message_id>/dislike', views.messages_dislike),
]
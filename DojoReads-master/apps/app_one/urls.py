from django.urls import path, include
from . import views

urlpatterns=[
    path('', views.index),
    path('join',views.join),
    path('login',views.verify),
    path('success',views.success),
    path('books',views.wall),
    path('logout',views.reset),
    path('books/add',views.add_book),
    path('add',views.add),
    path('books/<num>',views.book),
    path('review',views.review),
    path('users/<num>',views.user),
    path('delete',views.destroy),
    path('authors/<num>',views.author),
]
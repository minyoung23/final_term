from django.urls import path
from . import views

app_name='blog'

urlpatterns=[
    path('', views.post_table, name='post_table'),
    path('post/<int:pk>/',views.post_detail,name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
]
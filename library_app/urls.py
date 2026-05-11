from django.urls import path
from . import views

urlpatterns = [
    path('', views.books, name='books'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]